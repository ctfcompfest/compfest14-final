#!/bin/bash
docker-compose up -d

while true; do sleep 600; docker-compose down; docker-compose rm -f; docker-compose up -d; done
