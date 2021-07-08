#!/bin/bash
cd flask_app || exit

export FLASK_APP=ads.py

flask db upgrade
flask run --host=0.0.0.0