#!/bin/bash

if [ -z "$1" ]
  then
    echo "No url supplied"
fi

curl -H "Content-Type: application/json" -H "Authorization: NyaWDJekdjWI38KejJWlkd93jsdtu" -X POST -d '{"url":"'${1}'"}' http://localhost:8080/short_it/

echo ""