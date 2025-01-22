Prerequisites & Dependencies
============================

Before you create any projects with this template
--------------------------------------------------

* Ensure that your git is properly setup with your username and email in order for the initial commit to have the correct log.
* Project names must be composed of lowercase alphanumeric characters only, with no spaces or special characters.


Setting up for Installation
---------------------------

.. note::

    For Mac systems, there is an automatic installation script that handle dependencies for Hydra. Run the following commands to install via the script:

    .. code-block:: console

        $ git clone https://github.com/Lightmatter/django-hydra.git
        $ ./django-hydra/scripts/mac_intel_install.sh

    It's recommended that you read the output of this script to ensure everything went smoothly,
    particularly if you are using Apple silicone (Mac's with M1 or M2 chips).


Prerequisites
-------------

The following items are required in order for this template to work:

* `node <https://nodejs.org/en/download/>`_:
   * `npm <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_

* `python3 <https://www.python.org/downloads/>`_,
    * `pyenv <https://github.com/pyenv/pyenv>`_ is recommended to manage versions
    * `cookiecutter <https://cookiecutter.readthedocs.io/en/1.7.2/installation.html>`_

* `postgres <https://www.postgresql.org/download/>`_

*  bash (`WSL2 <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ or `Cygwin <https://cygwin.com/install.html>`_ recommended for windows users)
* `poetry <https://python-poetry.org/docs/>`_ virtual environment/package manager (python 3.10+ is required)
* `direnv <https://direnv.net/docs/installation.html>`_ handles activating your virtual env when you enter the project directory

.. _dependency-list:

Project Dependencies
--------------------

Hydra

* Python
* `Django <https://github.com/django/django/>`_: Django
* `whitenoise <https://github.com/evansd/whitenoise>`_: Static file servering for python web apps
* `django-allauth <https://github.com/pennersr/django-allauth>`_: Set of Django applications to address account management and authentication, including 3rd party auth
* `django-htmx <https://github.com/adamchainz/django-htmx>`_: Convenience methods for using HTMX with django, including CSRF token handling and partial rendering
* `django-annoying <https://github.com/skorokithakis/django-annoying>`_: Fixes for the annoying little things about Django
* `django-environ <https://github.com/joke2k/django-environ>`_: Allows for the configuration of a Django application using environment variables
* `django-extensions <https://github.com/django-extensions/django-extensions>`_: Extremely useful command extensions for debugging and development
* `django-model-utils <https://github.com/jazzband/django-model-utils>`_: Additional Django model mixins and utilities
* `psycopg2-binary <https://github.com/psycopg/psycopg2>`_: PostgreSQL database adapter for python
* `boto3 <https://github.com/boto/boto3>`_: AWS software development kit for python, allowing for use of S3 and EC2 technologies
* `django-storages <https://github.com/jschneier/django-storages>`_: A collection of custom storage backends for Django (Digitial Ocean, Dropbox, etc)
* `uvicorn <https://github.com/encode/uvicorn>`_: ASGI web server implementation for python
* `gunicorn <https://github.com/benoitc/gunicorn>`_: Lightweight Python WSGI HTTP server for UNIX
* `sentry-sdk <https://github.com/getsentry/sentry-python>`_: Sentry integration for Django for automatic error/exception reporting
* `Pillow <https://github.com/python-pillow/Pillow>`_: Library for adding image processing capabilities to the Python interpreter
* `django-anymail <https://github.com/anymail/django-anymail>`_: Extension for Django's core mailing feature that allows sending and receiving from several popular email service providers
* `django-vite <https://github.com/MrBin99/django-vite>`_: Plugin for using Vite in the Django ecosystem. For a detailed explanation of how Vite builds the frontend, see the Compiling and Deplyment section
* `tblib <https://github.com/ionelmc/python-tblib>`_: Serialization library for Exceptions and Tracebacks
* `redis <https://github.com/redis/redis>`_: Used for caching and as a message broker
* `hiredis <https://github.com/redis/hiredis>`_: C client library for Redis
* `django-redis <https://github.com/jazzband/django-redis>`_: Redis cache backend for Django that provides convenience methods for managing redis
* `django-jinja <https://github.com/niwinz/django-jinja>`_: Jinja2 integration for Django
* `heroicons <https://github.com/tailwindlabs/heroicons>`_: SVG icons library
* `django-rich <https://github.com/adamchainz/django-rich>`_: Rich is a library for producing vibrant command line applications, Django-Rich is the connecting extension


Dev Dependencies
^^^^^^^^^^^^^^^^

* `Werkzeug <https://github.com/pallets/werkzeug>`_: Simple WSGI server for local development, includes debugger, test client, and more
* `coverage <https://github.com/nedbat/coveragepy>`_: Utility for measuring code coverage testing
* `ipython <https://github.com/ipython/ipython>`_: IPython or Interactive Python is a command shell for python projects
* `ipdb <https://github.com/gotcha/ipdb>`_: Tool to export functions to the IPython debugger. See "debugging" section for more information on usage
* `ptpython <https://github.com/prompt-toolkit/ptpython>`_: An improved python repl with support for syntax highlighting, autocomplete, support for color schemes and more
* `django-debug-toolbar <https://github.com/jazzband/django-debug-toolbar>`_: Configurable set of panels to display debugging information about the current request/response
* `model-bakery <https://github.com/model-bakers/model_bakery>`_: Expedient tool for creating objects/fixtures for testing in Django
* `watchdog <https://github.com/gorakhargosh/watchdog>`_: Python API and shell utilities to monitor file system events.
* `honcho <https://github.com/nickstenning/honcho>`_: Python port of `Foreman <https://ddollar.github.io/foreman>`_, allows for a single command to launch Procfile based applications
* `unittest-xml-reporting <https://github.com/xmlrunner/unittest-xml-reporting>`_: Unit test runner that saves results to XML files for use on IDE's, continuous integration servers, etc
* `playwright <https://github.com/microsoft/playwright-python>`_: Browser automation for end-to-end testing
* `icecream <https://github.com/gruns/icecream>`_: Robust alternative to print statements in python for debugging
* `pre-commit <https://github.com/pre-commit/pre-commit>`_: framework for managing pre-commit hooks
* `pudb <https://github.com/inducer/pudb>`_: Alternative debugger, also integrates with IPython to give a more "GUI-like" experience to the user
* `poetryup <https://github.com/MousaZeidBaker/poetryup>`_: Version control helper that reconciles the pyproject.toml file each time `poetry update` is run
* `importmagic <https://github.com/alecthomas/importmagic>`_: Automatic management of imports in Python
* `epc <https://github.com/tkf/python-epc>`_: Allows for interoperability between Emacs and Python functions
* `django-silk <https://github.com/jazzband/django-silk>`_: Silk is a profiling and inspection tool for Django for HTTP requests and database queries
