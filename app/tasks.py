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

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

API = GoogleAPI()

@worker_ready.connect
def at_start(sender, **k):
    with app.app_context():
        #celery.add_periodic_task(30.0, update_data.s())
        data = API.update()
        keys = data.keys()
        pdate = date.today().strftime("%d/%m/%Y")
        url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + pdate
        values = xmltodict.parse(requests.get(url).content)['ValCurs']['Valute']
        rate = -1
        for val in values:
            if(val['Name'] == "Доллар США"):
                rate = float(val['Value'].replace(',', '.'))
                break
        for index, row in data.iterrows():
            new_entry = Entry(
                id=index,
                num=row[keys[1]],
                priced=float(row[keys[2]]),
                pdate=datetime.strptime(row[keys[3]], "%d.%M.%Y").strftime("%Y-%M-%d"),
                pricer=float(row[keys[2]])*rate
            )
            db.session.add(new_entry)
        db.session.commit()

@celery.task()
def update_data():
    data = API.update()
    keys = data.keys()
    date = date.today().strftime("%d/%M/%Y")
    url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date
    erate = xmltodict.parse(requests.get(url))
    value = float(erate['R01235']['Value'])
    for index, row in data.iterrows():
        new_entry = Entry(
            id=index,
            num=row[keys[1]],
            priced=row[keys[2]],
            pdate=row[keys[3]],
            pricer=row[keys[2]]*value
        )
        db.session.add(new_entry)
        i+=1
    db.session.commit()
    
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