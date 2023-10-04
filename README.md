# FLASK-STUDENT-MANAGEMENT

## Requirements

Python 3.8+

## Setup
- Duplicate the `.env_template` file and rename it to `.env`
- Ask a colleague for the values to fill your `.env`
## Basic installation
Install the pre-requirements for the postgresql adapter.
```bash
sudo apt-get update && apt-get install -y libpq-dev python3.8-dev
```

Install the required packages in your local environment (ideally virtualenv, conda, etc.).
```bash
pip install -r requirements/local.txt
```

## Instalation with docker-compose
```bash
docker-compose build
```

## Migrations

### Initialize database
```sh
flask db init
```
### Initialize database with docker-compose
```sh
docker-compose exec flask-api flask db init
```
### Create Migration
- First, create your models

```python
from app.db import db, BaseModelMixin

class MyModel(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    my_field = db.Column(db.String)

    def __init__(self, my_field):
        self.my_field = my_field

    def __repr__(self):
        return f'MyModel({self.my_field})'

    def __str__(self):
        return f'{self.my_field}'
```

- Run
```sh
flask db migrate
```
- Run with docker-compose
```sh
docker-compose exec flask-api flask db migrate
```

### Run Migrations

```sh
flask db upgrade
```

### Run Migrations with docker-compose
```sh
docker-compose exec flask-api flask db upgrade
```

## Project

### Run It

1. Start your app with:

```sh
flask run
```

2. Go to [http://localhost:8000/](http://localhost:8000/).

### Run with docker-compose

```sh
docker-compose up flask-api postgres
```

# Unit Tests
## Run unit tests

```sh
pytest
```

## Run unit tests with docker-compose
```sh
docker-compose exec flask-api pytest
```
