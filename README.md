# Server-side Catalog Item Rest API - FSND

> This web API is built with major libraries like Flask, Flask-RESTful, Flask-JWT, and Flask-SQLAlchemy, Flask-Script.

## Installation
#### Clone or download this project
```shell
git clone https://github.com/jerry-le/catalog-item-backend-api
```

#### Create virtual environment
Create a virtual environment from `requirements.txt` and enable it.
```shell
conda create -n flask-env python=3.5
pip install -r requirements.txt
source activate flask-env
```

#### Run migration
Before running server, we need to create database. To do this, we use Flask-Migrate to upgrade database from migration's revision
```
cd catalog-item-backend-api
python manage.py db upgrade
```
After upgrading you'll see `data.db` in root folder

#### Run server
```
python manage.py runserver --host 0.0.0.0 --port 5000
```

#### Run test
To make sure everything is woking fine, we need to run tests.
```
python manage.py test
```
If every tests pass, move to next step
