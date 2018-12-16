#!/usr/bin/env bash
flask db upgrade
flask translate compile
exec gunicorn -b :443 --access-logfile - --error-logfile - main:app
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=microblog -e MYSQL_USER=root \
    -e MYSQL_PASSWORD=\
    mysql/mysql-server:5.7