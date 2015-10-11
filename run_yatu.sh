docker-compose kill

docker-compose up -d db

docker build -t yatu_liquibase ./apps/db-schema
docker-compose run --rm liquibase liquibase_update

./run_api.sh