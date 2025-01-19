Project Structure
==============================

Hydra is wholly contained within the Django project folder. All of the backend functionality is defined in apps within the project folders, html/jinja templates and Alpine.js components for additional frontend functionality are defined side by side within a templates folder, and the static assets (such as CSS and TypeScript) that are served by Vite are defined in the static_source. The philosophy is to have things that are related to each other actually next to each other and not have a separate frontend vs backend folder structure.

The folder structure within ``/{{ cookiecutter.project_name }}``  is as follows:

* ``/config`` - Project settings, asgi settings, and base urls
* ``/home`` - Handles home page for django, error endpoint, settings context processor
* ``/user`` - User related logic, views, models, etc.
* ``/util`` - Container for general utility classes, functions, etc.
* ``/static`` - Created by ``./manage.py collectstatic`` stores static assets added to ``/static_source`` to be served at runtime
* ``/static_source`` - contains static assets (such as CSS and TypeScript) that will be served by Vite
    * ``/js``- The Alpine.js project root
* ``/templates`` - html/jinja templates for all webpages served by the app and Alpine.js components


Backend
-------

Hydra relies on much of Django's default tooling with some packages added on to allow for extensibility and ease of use, including
    * `django-annoying <https://github.com/skorokithakis/django-annoying>`_
    * `django-extensions <https://github.com/django-extensions/django-extensions>`_
    * `django-model-utils <https://github.com/jazzband/django-model-utils>`_

For a complete list of the dependencies used and the purpose for their inclusion, check :ref:`dependency-list`


Frontend
--------

Vite.js
*******
Hydra uses Vite to bundle the frontend libraries and frameworks, as well as handling for static assets.

Vite leverages the fact that modern browsers support module imports natively, meaning that when files are served
the browser makes the HTTP requests for each import and then the dev server receives the browser's HTTP requests and
makes any changes by hotswapping code.

The hotswapping support for Hydra's Jinja templates are handled by `django-vite <https://github.com/MrBin99/django-vite>`_,
specifically the `vite_hmr_client tag <https://github.com/MrBin99/django-vite#template-tags>`_.

Configuration of Vite is explored in more detail in the Compiling and Deployment section

Templates
*********
Jinja templating provides powerful, but easy to implement methods for reducing code and producing easily maintainable templates, but there's a few concepts
that are worth keeping in mind as you work with it

How Jinja Works:
^^^^^^^^^^^^^^^^

Jinja template inheritance functions very similarly to `Django's templates <https://docs.djangoproject.com/en/4.0/ref/templates/language/>`_.
Just like Django templates, you can extend a template and have the child template inherit from the base or parent template, and overwrite blocks of
content.

Jinja `macros <https://jinja.palletsprojects.com/en/3.1.x/templates/#macros>`_ are a powerful way to reduce code and template specific components for reuse.
They can be thought of as functions that return customized templates based off of whatever arguments are passed to them. Much like functions, they are declared and then called.

The declaration for a link macro may look like the following:

.. code-block:: html+django
    :caption: .../components/link.jinja

    {% macro link(url, text='', target='') %}
        <a href="{{ url }}"
        target="{{ target }}"
        class="text-blue-500; hover:text-blue-700; underline">{{ text }}</a>
    {% endmacro %}

Then, when the macro is called in a template file, you'll see something akin to the following:

.. code-block:: html+django

    {% from 'components/link.jinja' import link %}

    <body>
        ...
        {% set url='https://www.google.com' %}
        {% set text='A ubiquitous search engine' %}
        {% set target='blank' %}

        <div class='link-container'>
            {{ link(url, text, target) }}
        </div>

    </body>


Alpine JS and HTMX:
^^^^^^^^^^^^^^^^^^^
Both Alpine.js and HTMX are libraries designed to reduce the amount of vanilla Javascript being written by allowing you to tie common actions directly to the DOM element they are affecting.

It's highly recommended to read through the documentation for both `Alpine <https://alpinejs.dev/start-here>` and `HTMX <https://htmx.org/docs/>` to familiarize yourself with
the mechanics of how these technologies work, but their basic use will be very briefly outlined below.

Essentially (and somewhat reductively), HTMX allows for HTML elements to submit AJAX requests, and Alpine takes care of everything else that Javascript typically would.

It's important to note that any endpoint you are using with HTMX must return the HTML you are either adding or replacing on the page.

For instance, let's say that we wanted to add an element to a page on a button click.

.. code-block:: html+django

    <div>
        <button hx-get="/add-paragraph" hx-target=".lorem-ipsum-container" hx-swap="beforeend">
            Add Text
        </button>
    </div>

    <div class="lorem-ipsum-container">
    </div>

In this case, we have a get request that is fired to the `/add-paragraph` endpoint. We use `hx-target` and `hx-swap` to ensure that each piece of HTML is appended to the content of the
`lorem-ipsum-container` div. The default behavior for a swap is to replace all of the interior content of the targeted element.

Now let's say that we wanted to count how many times the user had clicked to add paragraphs to the `lorem-ipsum-container` - we could do that with Alpine.

.. code-block:: html+django

    <div x-data="{timesClicked: 0}">
        <button
            hx-get="/add-paragraph"
            hx-target=".lorem-ipsum-container"
            hx-swap="beforeend"
            x-on:click="timesClicked+=1"
        >
            Add Text
        </button>
        <p x-text="timesClicked"></p>
    </div>

    <div class="lorem-ipsum-container">
    </div>

With the `@click` event (a piece of syntactic shorthand for `x-on:click`), the piece of data belonging to the parent div will be incremented. The `x-text` attribute ties the value of the piece of
Alpine data `timesClicked` to the innerHTML of the `<p>` tag. There is more that could be done here, for example, only displaying the `timesClicked` if the amount is greater than zero, limiting
the amount of times that the button could be clicked, all of which is possible with Alpine.

One other thing worth keeping in mind with Alpine: the scope of `timesClicked` is available only to the child elements of the div where it is defined. This
`does work <https://alpinejs.dev/directives/data#scope>`_ with nested components.


Tailwind CSS:
^^^^^^^^^^^^^

`Tailwind CSS <https://tailwindcss.com/>`_ is a framework that allows developers to compose CSS directly into the class attribute
of HTML elements.

One important thing to note is that Tailwind does have a default color palette that can be referenced `here <https://tailwindcss.com/docs/customizing-colors>`_

For instructions on customizing or extending the color palette, see the instructions in the link above.

.. note::

    Because of how Vite and Tailwind compile and run, Tailwind classes that only appear in dynamically generated code from the server may not work as expected.
    See this `Stack Overflow post <https://stackoverflow.com/questions/70907369/color-classes-of-tailwind-css-not-working-when-appended>`_ for more details

Components
----------

All generic Jinja components are under the `{{cookiecutter.project_name}}/templates/components/` directory. The structure follows the
material.ui format of having a folder per component with the js/css/jinja files within, allowing for files to be overwritten and customized
as needed.


Forms
-----

It's important to note that the widgets that django typically provides are overwritten in Hydra. Rather than working directly with the Django widgets as they as written,
the Jinja templates for widgets are imported as the defaults. Due to how Django requires that the component templates are overwritten by shadowed methods,
you'll see several examples of this under the ``templates/django/forms/widgets/`` directory.

New custom form widgets can be composed using Jinja and shadowed in a similar manner.
To reference the django widgets, see the `widgets folder in the Django repository <https://github.com/django/django/tree/main/django/forms/templates/django/forms/widgets>`_
