#!/bin/bash
uwsgi --http :8080 --wsgi-file apps/api/src/app.py --callable=appl --python-auto-reload 1