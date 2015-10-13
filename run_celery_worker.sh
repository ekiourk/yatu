#!/bin/bash
celery -A yatu.celery worker --loglevel=info
