#!/bin/bash
uwsgi --http :8080 --wsgi-file api/src/app.py --callable=appl --python-auto-reload 1 --pythonpath api/src/