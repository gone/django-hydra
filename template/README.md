# {{ cookiecutter.project_name_verbose }}

## Overview
{{ cookiecutter.description }}

# Project Structure
This project is divided into 2 major parts: Alpine.js to provide additional front end functionality and a Django backend.
It's the Django server is deployed with precompiled static assets

- `/{{ cookiecutter.project_name }}` - the Django project folder
    - `/config` - Project settings, asgi settings, and base urls
    - `/home` - Handles home page for django, error endpoint, settings context processor
    - `/user` - User related logic, views, models, etc.
    - `/util` - Container for general utility classes, functions, etc.
    - `/static_source` - for adding assets that will be served via python, Alpine.js project root, contains static assets (such as CSS and TypeScript) that will be served
    - `/templates` - html/htmx templates for all webpages served by the app

# Getting Started

These instructions will help you get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites
* [node](https://nodejs.org/en/download/)
  * [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [python3 (preferrably python 3.10)](https://www.python.org/downloads/), although [pyenv](https://github.com/pyenv/pyenv) is recommended to manage versions
* [git](https://git-scm.com/downloads)
* bash ([WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) or [Cygwin](https://cygwin.com/install.html) recommended for windows users)
* [postgres](https://www.postgresql.org/download/)
* [poetry](https://python-poetry.org/docs/) virtual environment/package manager
* [direnv](https://direnv.net/docs/installation.html) handles activating your virtual env when you enter the project directory

### macOS

Below is a sample configuration for macOS 11 Big Sur, but it should mostly work for any linux, unix, *nix based distribution.

#### Dependencies

* It is highly recommended to install the above dependencies, as well as anything below via homebrew. If you do not have homebrew, get the install command [here](https://brew.sh/)
* You likely need to install libpq-dev, `brew install libpq-dev`, although if you install with homebrew it will have installed this already most likely. If your postgres instance is not working, run this command.
* For file watching and debugging, install [watchman](https://facebook.github.io/watchman/). `brew install watchman`
* You will likely need GSL as well, `brew install gsl`.
* You will need to install Poetry (which requires python 3.10 or greater at the moment), `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -`
    * In order for poetry to run on the correct python version, you will want to make sure that python3 resolves to python 3.10 in your shell
* you will need to install direnv, `brew install direnv` and follow the shell specific instructions here <https://direnv.net/docs/hook.html>

You must have postgres, python, poetry, and direnv ready to go on your system.

#### Run-commands / profile

You should have the following in your `.bashrc` or `.zshrc` or equivalent.

1. Setup the Path Variable (This is for Pyenv)

```bash
# PATH definition using Pyenv
export PATH="$(pyenv root)/shims:$PATH"
```

2. Trigger pyenv, direnv inits, add poetry to PATH.
```bash
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(direnv hook zsh)"
export PATH="$HOME/.poetry/bin:$PATH"
```

* the direnv command will be slight different depending on your shell, follow the instructions at <https://direnv.net/docs/hook.html>

3. Set up the environment variables for Postgres
```bash
alias pg_start="launchctl load ~/Library/LaunchAgents"
alias pg_stop="launchctl unload ~/Library/LaunchAgents"
export PGDATA="/usr/local/var/postgres/"
```

4. If you had to install the Gnu-scientific-library (GSL), setup the library path and the following environment variables.
```bash
export LIBRARY_PATH=/usr/local/Cellar/gsl/2.7/lib/

export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

### Windows

#### Dependencies
* You will need to install Poetry (which requires python 3.10 or greater at the moment), `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python3 -` n.b. if you are using a bash shell, you should run the version of this command in the macOS section above
    * In order for poetry to run on the correct python version, you will want to make sure that python3 resolves to python 3.10 in your shell

### Not macOS (including Windows)

#### Dependencies
* You will need to install direnv, platform specific installation instructions are available here <https://direnv.net/docs/installation.html>



## Local Development Initial Setup
Run the below commands in order:
The recommended start pattern is described below. The setup_existing_project.sh command will
* install python and js requirements (dev and regular) via poetry and (or optionally yarn)
* create a database
* run the migrations
* and setup git
1. Grant permissions to the `setup_existing_project.sh`
```bash
$ chmod +x ./scripts/setup_existing_project.sh
```
2. Execute the `setup_existing_project` script
```bash
$ ./scripts/setup_existing_project.sh
```
3. Run Django server with runserver_plus
```bash
$ ./manage.py runserver_plus
```
4. In a new shell tab/window navigate to the project directory and run the vite server with npn run dev
```bash
$ npm run dev
```
5. You will now be able to view the project at http://127.0.0.1:8000/ or http://localhost:8000

#### Quick start
In order to be able to run these commands, you must have previously run the full initial setup including `setup_existing_project.sh` above
1. Run Django server with runserver_plus
```bash
$ ./manage.py runserver_plus
```
2. In a new shell tab/window navigate to the project directory and run the vite server with npn run dev
```bash
$ npm run dev
```
3. You will now be able to view the project at http://127.0.0.1:8000/ or http://localhost:8000

# Configuring environment variables

Before you may develop on the app itself you will need a `.env` file. Provided in the template is a `.env.example` which can be copy and pasted into a new .env file. It is worth noting that when a new project is created via `create_new_project.sh`, the `.env.example` will be copied to new instance under `.env`. This template leverages this file using the dotenv JavaScript library as part of Vite.

## Accessing Environment Variables in Python
Env vars are available in all settings file, more details here <https://django-environ.readthedocs.io/en/latest/index.html>

## Accessing Environment Variables in JavaScript/TypeScript
Env vars are available in all .js files and html script tags using the global var import.meta.env.{VARIABLE_NAME}, more details here <https://vitejs.dev/guide/env-and-mode.html>

# Debugging
To access a python shell pre-populated with Django models and local env
```bash
$ ./manage.py shell_plus
```
To add a breakpoint in your python code:
Add the following code to your `.bashrc` or `.zshrc`:
```bash
$ export PYTHONBREAKPOINT="pudb.set_trace"
```
Then add the following to your python code:
```python
breakpoint()
```
If the above fails or you prefer a more immediate solution, you can add the following to your code:
```python
import pudb; pu.db
```

# Testing/Validation
This will be run automatically when you attempt to commit code but if you want to manually validate/fix your code syntax during development you can run
```bash
$ poetry run pre-commit run --all-files
```

Django tests can be run by running
```bash
$ pytest
```
# Deployment/Predeployment
This will be run automatically when you attempt to commit code but if you want to manually validate/fix your code syntax during development you can run
```bash
$ poetry run pre-commit run --all-files
```

This app is set up to use circleci, but could be extended to any build process. Circle will automatically run

```bash
$ poetry run pre-commit run --all-files
$ poetry run playwright install
$ poetry run coverage run --source='.' -m pytest
```
#### This app is also set up to deploy to render, which is configured via the `render.yaml` file
It creates:
* a Django webserver with a prebuilt/precompiled front end
* a Minio service that manages media asset storage on AWS S3
* a redis service
* a PostgreSQL database


## Multiple domain setup process

The app is capable of working with a multi-domain setup. Use case: App A has a django backend and a react native frontend. App B also uses App A's backend but is not hosted on the same domain.

ALLOWED_HOSTS setting  must look something like `ALLOWED_HOSTS=127.0.0.1:3000|localhost:3000|localhost:3001|.ngrok.io` (locally) and similar on render. Every domain that connects to the backend needs to be in allowed hosts.
`CSRF_COOKIE_DOMAIN = env("CSRF_COOKIE_DOMAIN")` the CSRF cookie domain env variable is important to allow POST requests to work coming from the secondary app. This can be set to a subdomain like `.exampleapp.com`
`CORS_ALLOWED_ORIGINS` and CSRF_TRUSTED_ORIGINS both pull from allowed hosts and are crucial for this process.


## Differences between Local and Remote
- Emails:
    - Emails will be printed to the console when being "sent" during local development
    - Emails will be pushed to a third party service for sending on the remote server (n.b. this must be set up separately and configured through the relevant Django settings)
- Static/Media Assets:
    - Static assets are compiled on render and may be cached but are not locally
    - Media assets are stored in an AWS S3 bucket on render as opposed to being stored in the media folder within the project during local development

## Useful Commands
NOTE: you must be at the project root to run any `./manage.py ...` or `./scripts/...` commands

### AWS
- Retrieve Media assets from AWS S3:
    - Set up and configure the AWS CLI: see <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html> for instructions
        - be sure to set up your AWS config with your {{ cookiecutter.project_name }} credentials: instructions here <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>
    - make sure a directory exists with the path [project root]/{{ cookiecutter.project_name }}/media
    - from the project root run: `aws s3 cp s3://{{ cookiecutter.project_name }}-dev ./{{ cookiecutter.project_name }}/media --recursive` replacing `{{ cookiecutter.project_name }}-dev` with `{{ cookiecutter.project_name }}-prod` or a different s3 bucket name as needed

## Styleguide

TODO storybook

---
TO ADD


documentation
### record myself adding a component
  - Django component py file
  - Template creation in dedicated file
     -  Does it exist in a third party component lib? (Alpinejs or TailwindUI) - move relevant parts in
  - TS in frontend
  - Using it in a template
### DIRENV
### PLAYWRIGHT
webcomponents w/ alpine
Alpine dev tools



Features:
 get transitions between active states working in header

### UPGRADING PYTHON PACKAGES
https://github.com/python-poetry/poetry/issues/1387
###UPGRADING NODE PACKAGES
https://shouts.dev/upgrade-all-npm-packages-to-the-latest-versions
