#!/bin/bash

curl -H "Content-Type: application/json" -H "Authorization: NyaWDJekdjWI38KejJWlkd93jsdtu" -X GET http://localhost:8080/short_urls/$1

echo ""