#!/bin/bash


export ENV_NAME="{{cookiecutter.project_name}}"

dropdb $ENV_NAME
heroku pg:pull DATABASE_URL $ENV_NAME --app $ENV_NAME-development
for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" $ENV_NAME` ; do  psql -c "alter table \"$tbl\" owner to $ENV_NAME" $ENV_NAME ; done
for tbl in `psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = 'public';" $ENV_NAME` ; do  psql -c "alter table \"$tbl\" owner to $ENV_NAME" $ENV_NAME ; done
