#!/usr/bin/env bash
flask db stamp head 
flask db migrate
flask db upgrade 
flask run --host=0.0.0.0 --port=3001