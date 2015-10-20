#!/bin/bash
docker-compose kill

docker-compose up -d db rabbitmq

docker build -t yatu_liquibase ./db-schema
docker-compose run --rm liquibase liquibase_update

./run_api.sh
