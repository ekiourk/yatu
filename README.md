# YATU (Yet Another Tiny URL)

[![Build Status](https://travis-ci.org/ekiourk/yatu.svg?branch=master)](https://travis-ci.org/ekiourk/yatu)

### How do I run YATU locally?

You need to have python3, [docker](https://docs.docker.com/installation/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system


1. Create yourself a Python3 virtual environment: `virtualenv -p python3 ~/yatu_env`
2. Activate the virtualenv: `source ~/yatu_env/bin/activate`
3. Install all requirements by calling `./install_requirements.sh` from the root of the project
4. Call `./run_yatu.sh` from the root of the project. This will bring up postgres, rabbitmq and will run the api server. It will also make sure the database schema is updated
5. In another terminal activate virtualenv again and call `./run_celery_worker.sh` from the root of the project

### How do I run the tests?

1. First run YATU locally by following the steps above
2. In a new terminal activate virtualenv
3. Call `run-contexts apps/tests/src` for the unitests
4. Call `run-contexts apps/acceptance/src` for the integration tests

### Why Rabbit and celery?

The target is to have a fast response time on the requests of short urls. At the same time we want to keep statistics for each request to the api. In order to not block the api till the statistics are processed and stored, we need celery to publish a task to deal with statistics in an asynchronous manner.

### TODO:

Add redis to store only the short_url - long_url pair and use that to resolve the short urls for even faster response times 