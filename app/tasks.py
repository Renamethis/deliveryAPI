from turtle import update
from .extensions import celery, db
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from .database.models import Entry
from .googleapi.google_api import GoogleAPI
import xmltodict
from datetime import date, datetime
import requests
from . import create_app
import os 
import pandas as pd
from celery.utils.log import get_task_logger

# Constants
PRICE_RUB_COLUMN = "стоимость,₽"
VALUTE_NAME =  "Доллар США"

# Initialize app with factory
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

logger = get_task_logger(__name__)

# Initialize google API class
API = GoogleAPI()

# Configure Celery periodic task
celery.conf.beat_schedule = {
    'update_task': {
        'task': 'app.tasks.update',
        'schedule': 5.0,
    },
}
celery.conf.timezone = 'UTC'

# Periodic task to update database
@celery.task
def update():
    with app.app_context():
        data = API.update()
        keys = list(data.keys())
        keys.append(PRICE_RUB_COLUMN)
        entries = Entry.query.all()
        # Format data from database 
        from_db = [list(entry.to_json().values()) for entry in entries]
        for d in from_db:
            d[3] = d[3].strftime("%d.%m.%Y")
        from_db = pd.DataFrame(from_db, columns=keys)
        from_db = from_db.drop(PRICE_RUB_COLUMN, 1)
        if(not from_db.equals(data)):
            # Erase database 
            Entry.query.delete
            # Get valute rate
            pdate = date.today().strftime("%d/%m/%Y")
            url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + pdate
            values = xmltodict.parse(requests.get(url).content)['ValCurs']['Valute']
            rate = -1
            for val in values:
                if(val['Name'] == "Доллар США"):
                    rate = float(val['Value'].replace(',', '.'))
                    break
            # Add new information in database
            for _, row in data.iterrows():
                new_entry = Entry(
                    id=row[keys[0]],
                    num=row[keys[1]],
                    priced=float(row[keys[2]]),
                    pdate=datetime.strptime(row[keys[3]], "%d.%m.%Y").strftime("%Y-%m-%d"),
                    pricer=float(row[keys[2]])*rate
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