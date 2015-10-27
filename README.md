# YATU (Yet Another Tiny URL)

[![Build Status](https://travis-ci.org/ekiourk/yatu.svg?branch=master)](https://travis-ci.org/ekiourk/yatu)

### How do I run YATU locally?

You need to have python3, [docker](https://docs.docker.com/installation/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system

1. Create yourself a Python3 virtual environment: `virtualenv -p python3 ~/yatu_env`
2. Activate the virtualenv: `source ~/yatu_env/bin/activate`
3. Install all requirements by calling `./install_all_requirements.sh` from the root of the project
4. Call `./run_yatu.sh` from the root of the project. This will bring up postgres, rabbitmq and will run the api server. It will also make sure the database schema is updated
5. In another terminal activate virtualenv again and call `./run_celery_worker.sh` from the root of the project

### How do I run YATU inside docker containers

You need to have [docker](https://docs.docker.com/installation/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system

1. Call the `run_yatu_inside_docker.sh` script and wait till it finishes building everything, running migrations and bringing up the api on (http://localhost:8080)[http://localhost:8080].

After the above step finishes, you are ready to use the system. Use the helper scripts on the curl_scripts directory to post urls to be shorted and to retrieve information by using the token of the yatu user that already exists in the database. 

### How do I run the tests?

Follow the steps.
NOTE: If you want to run YATU inside containers, you still need to create and activate a virtual env and install requirements in order to run the tests

1. First run YATU either locally or inside docker by following the steps above
2. In a new terminal activate virtualenv
3. Call `run-contexts -v tests/unitests` for the unitests
4. Call `run-contexts -v tests/integration` for the integration tests

### Directory structure

The main cadebase leaves in the yatu python package and can be found at base/yatu/
The API is located in the api/ and it is a very simple codebase with only the api endpoints and the views.
The unit and integration tests can be found in tests/ directory 
Last but not least is the db schema migrations (db-schema). For that we are using liquibase which is dockerised. By building and running the docker container, it connects to the database and makes sure that the schema is up to date

### Why Rabbit and celery?

The target is to have a fast response time on the requests of short urls. At the same time we want to keep statistics for each request to the api. In order to not block the api till the statistics are processed and stored, we need celery to publish a task to deal with statistics in an asynchronous manner.

### TODO

- [ ] Add redis to store only the short_url - long_url pair and use that to resolve the short urls for even faster response times
- [ ] Add api for user registration and access token management
- [ ] Hash the user passwords in the database