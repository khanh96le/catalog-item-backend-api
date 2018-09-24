# Server-side Catalog Item Rest API

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

#### Run server
```
(flask-env) export FLASK_APP=autoapp.py
(flask-env) export FLASK_DEBUG=1
(flask-env)flask run --with-threads
```

#### Run test
```
(flask-env) flask test
```

#### Show all available endpoints
```
(flask-env) flask urls
```
