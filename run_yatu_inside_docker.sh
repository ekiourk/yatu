#!/bin/bash

docker build -t yatu_base apps/base

docker-compose build

docker-compose run --rm liquibase liquibase_update

docker-compose up api