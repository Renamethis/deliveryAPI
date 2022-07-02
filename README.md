# deliveryAPI
This application contains frontend and backend for delivery database management from Google Sheets.

The information in the database is updated every 30 seconds using celery periodic tasks.

The notification about the delivery time exceeded comes when the server is initialized and then every time the database is updated (In case there are new records with a delivery time that has expired).
Google Sheets document: https://docs.google.com/spreadsheets/d/16CiACm_JccpThKOz7TQxK95x129l6g0XosSr7DG6pfM/edit?usp=sharing
# Tech
- Flask web-framework
- SQLAlchemy library 
- PostgreSQL DBMS
- Celery task queue
- Redis DBMS
- Telegram, Google API
- React frontend framework
- Docker
# Deploy
Build and docker containers:
```bash
docker-compose up -d --remove-orphans --build
```
Stop and remove docker containers:
```bash
docker-compose down --remove-orphans
```

Check all running containers:
```bash
docker ps -a
```
Check logs of docker-container:
```bash
docker logs --tail {amount of last rows} --follow --timestamps {container_name}
```
# Usage
To go on react web-page go to http://localhost:3000/ address in your browser.

To test flask-API go to http://localhost:5000/entries or http://localhost:5000/entries/chart address in browser or send GET-request.
