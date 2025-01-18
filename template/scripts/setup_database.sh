#!/bin/bash

# What you care about is at the end of the file :)

RED='\033[0;31m'
YELLOW='\033[1;33m'
CLEAR='\033[0m'

check_db_perms() {
  # does shell scripting always feel like a hack?
  _=`psql postgres --command='\du' > /dev/null 2>&1`

  if [ $? -ne 0 ]
  then
    printf "${RED}Current user \"${USER}\" is not correctly configured for psql${CLEAR}\n"
    exit 1
  fi
}

insert_db_user() {
  printf "${YELLOW}Attempting to create psql user w/ sudo...${CLEAR}\n"

  # user name gets messy when using su
  CREATE="create role ${USER} with createdb login;"
  SET_SU="alter user ${USER} superuser;"
  MAKE_DB="create database ${USER} with owner ${USER};"
  sudo su postgres --session-command="psql --command='${CREATE}'" 1> /dev/null
  sudo su postgres --session-command="psql --command='${SET_SU}'" 1> /dev/null
  sudo su postgres --session-command="psql --command='${MAKE_DB}'" 1> /dev/null
}

setup_db() {
  #TODO: This doesn't handle test databases correctly
  RESULT=`psql -l | grep "{{ cookiecutter.repo_name }}" | wc -l`
  if test $RESULT -eq 0; then
      echo "Creating Database";
      psql -c "create role {{ cookiecutter.repo_name }} with createdb encrypted password '{{ cookiecutter.repo_name }}' login;"
      psql -c "alter user {{ cookiecutter.repo_name }} superuser;"
      psql -c "create database {{ cookiecutter.repo_name }} with owner {{ cookiecutter.repo_name }};"
  else
      echo "Database exists"
  fi
}

setup_tables() {
  poetry run python manage.py migrate
}

#
# < the part that matters >
#

result=`check_db_perms`
return_code=$?

echo "${result}" # expand new lines

if [ $return_code -ne 0 ]
then
  # assume the perms check failed
  insert_db_user &&\
    setup_db &&\
    setup_tables
  exit 0
fi

setup_db && setup_tables

#
# </ the part that matters >
#
