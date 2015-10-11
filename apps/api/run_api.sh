#!/bin/bash
uwsgi --http :8080 --wsgi-file src/app.py --callable=appl --python-auto-reload 1