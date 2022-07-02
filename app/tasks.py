from turtle import update
from .extensions import celery, db
from .database.models import Entry
from .googleapi.google_api import GoogleAPI
from celery.utils.log import get_task_logger
from .bot import TelegramBot
import xmltodict
from datetime import date, datetime
import requests
from . import create_app
import os 
import pandas as pd

# Constants
PRICE_RUB_COLUMN = "стоимость,₽"
EXPIRED_COLUMN = "срок пройден"
VALUTE_NAME =  "Доллар США"

# Initialize app with factory
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Initialize google API class
API = GoogleAPI()

# Configure Celery periodic task
celery.conf.beat_schedule = {
    'update_task': {
        'task': 'app.tasks.update',
        'schedule': 30.0,
    },
}
celery.conf.timezone = 'UTC'
logger = get_task_logger(__name__)

# Periodic task to update database
@celery.task
def update():
    with app.app_context():
        data = API.update()
        keys = list(data.keys())
        keys.append(PRICE_RUB_COLUMN)
        keys.append(EXPIRED_COLUMN)
        entries = Entry.query.all()
        # Format data from database 
        from_db = [list(entry.to_json().values()) for entry in entries]
        for d in from_db:
            d[3] = d[3].strftime("%d.%m.%Y")
        from_db = pd.DataFrame(from_db, columns=keys)
        for_comprasion = from_db.drop(columns=[PRICE_RUB_COLUMN, 
                                               EXPIRED_COLUMN], axis=1)
        if(not data.equals(for_comprasion)):
            # Erase database 
            Entry.query.delete
            # Get valute rate
            pdate = date.today().strftime("%d/%m/%Y")
            url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + pdate
            values = \
                xmltodict.parse(requests.get(url).content)['ValCurs']['Valute']
            rate = -1
            for val in values:
                if(val['Name'] == "Доллар США"):
                    rate = float(val['Value'].replace(',', '.'))
                    break
            # Set index to number of entry
            data = data.set_index(keys[0])
            from_db = from_db.set_index(keys[0])
            # Add new information in database
            for index, row in data.iterrows():
                today = date.today()
                # Check if date is expired and send telegram message
                if(not from_db.empty and index in from_db.index):
                    is_expired = from_db.loc[index][4]
                else:
                    is_expired = False
                if(datetime.strptime(row[keys[3]], "%d.%m.%Y").date() < today \
                    and not is_expired):
                    bot = TelegramBot()
                    bot.send_text("У поставки №" + str(row[keys[1]]) + \
                        " вышел срок исполнения.")
                    is_expired = True
                if(not index in from_db.index):
                    # New database entry
                    new_entry = Entry(
                        id=index,
                        num=row[keys[1]],
                        priced=float(row[keys[2]]),
                        pricer=float(row[keys[2]])*rate,
                        expired=is_expired,
                        pdate=datetime.strptime(row[keys[3]],
                                                "%d.%m.%Y").strftime("%Y-%m-%d")
                    )
                    db.session.add(new_entry)
            db.session.commit()

# Celery task to read information from database
@celery.task()
def get(id):
    if(id == None):
        entries = Entry.query.all()
        data = [entry.to_json() for entry in entries]
        for d in data:
            d['date'] = d['date'].strftime("%Y-%m-%d")
        return data
    else:
        entry = Entry.query.get(id)
        if(entry is None):
            return None
        else:
            entry = entry.to_json()
            entry['date'] = entry['date'].strftime("%Y-%m-%d")
            return entry

# Celery task to get dates and prices for chart building
@celery.task()
def chart():
    dates = [entry.pdate.strftime("%d/%m/%Y") for entry in \
        Entry.query.order_by(Entry.pdate).all()]
    prices = [entry.priced for entry in Entry.query.order_by(Entry.pdate).all()]
    return dates, prices