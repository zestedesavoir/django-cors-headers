|Build Status| |codecov.io|

|PyPI|

django-cors-middleware
======================

A Django App that adds CORS (Cross-Origin Resource Sharing) headers to
responses.

Although JSON-P is useful, it is strictly limited to GET requests. CORS
builds on top of XmlHttpRequest to allow developers to make cross-domain
requests, similar to same-domain requests. Read more about it here:
http://www.html5rocks.com/en/tutorials/cors/

This is a fork of `https://github.com/ottoyiu/django-cors-headers/`_
because of inactivity.

Supported versions of Python and Django :

+------------------+--------------+--------------+--------------+--------------+
|                  | **Py 2.7**   | **Py 3.3**   | **Py 3.4**   | **Py 3.5**   |
+==================+==============+==============+==============+==============+
| **Django 1.8**   | YES          | YES          | YES          | YES          |
+------------------+--------------+--------------+--------------+--------------+
| **Django 1.9**   | YES          |              | YES          | YES          |
+------------------+--------------+--------------+--------------+--------------+
| **Django 1.10**  | YES          |              | YES          | YES          |
+------------------+--------------+--------------+--------------+--------------+

Setup
-----

Install by downloading the source and running:

    python setup.py install

or

    pip install django-cors-middleware

and then add it to your installed apps:

::

    INSTALLED_APPS = (
        ...
        'corsheaders',
        ...
    )

You will also need to add a middleware class to listen in on responses:

::

    # Use `MIDDLEWARE_CLASSES` prior to Django 1.10
    MIDDLEWARE = [
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    ]

Note that ``CorsMiddleware`` needs to come before Django’s
``CommonMiddleware`` if you are using Django’s ``USE_ETAGS = True``
setting, otherwise the CORS headers will be lost from the 304
not-modified responses, causing errors in some browsers.

Signals
-------

If you have a use-case that requires running Python code to check if a site exists,
we provide a Django signal that covers this.
We have a ``check_request_enabled`` signal that provides the request.
Here is an example configuration::

    from corsheaders import signals
    from .models import Site

    def handler(sender, request, **kwargs):
        for site in Site.objects.all():
            if request.host in site.domain:
                return True
        return False

    signals.check_request_enabled.connect(handler)

If the signal returns ``True``,
then the request will have headers added to it.

Configuration
-------------

Add hosts that are allowed to do cross-site requests to
``CORS_ORIGIN_WHITELIST`` or set ``CORS_ORIGIN_ALLOW_ALL`` to ``True``
to allow all hosts.

``CORS_ORIGIN_ALLOW_ALL``
~~~~~~~~~~~~~~~~~~~~~~~~~

If True, the whitelist will not be used and all origins will be accepted

Default:

::

    CORS_ORIGIN_ALLOW_ALL = False

``CORS_ORIGIN_WHITELIST``
~~~~~~~~~~~~~~~~~~~~~~~~~

Specify a list of origin hostnames that are authorized to make a
cross-site HTTP request

Example:

::

    CORS_ORIGIN_WHITELIST = (
        'google.com',
        'hostname.example.com'
    )

Default:

::

    CORS_ORIGIN_WHITELIST = ()

``CORS_ORIGIN_REGEX_WHITELIST``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify a regex list of origin hostnames that are authorized to make a
cross-site HTTP request; Useful when you have a large amount of
subdomains for instance.

Example:

::

    CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(\w+\.)?google\.com$', )

Default:

::

    CORS_ORIGIN_REGEX_WHITELIST = ()

--------------

You may optionally specify these options in settings.py to override the
defaults. Defaults are shown below:

``CORS_URLS_REGEX``
~~~~~~~~~~~~~~~~~~~

Specify a URL regex for which to enable the sending of CORS headers;
Useful when you only want to enable CORS for specific URLs, e. g. for a
REST API under ``/api/``.

Example:

::

    CORS_URLS_REGEX = r'^/api/.*$'

Default:

::

    CORS_URLS_REGEX = '^.*$'

``CORS_ALLOW_METHODS``
~~~~~~~~~~~~~~~~~~~~~~

Specify the allowed HTTP methods that can be used when making the actual
request

Default:

::

    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )

``CORS_ALLOW_HEADERS``
~~~~~~~~~~~~~~~~~~~~~~

Specify which non-standard HTTP headers can be used when making the
actual request

Default:

::

    CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken'
    )

``CORS_EXPOSE_HEADERS``
~~~~~~~~~~~~~~~~~~~~~~~

Specify which HTTP headers are to be exposed to the browser

Default:

::

    CORS_EXPOSE_HEADERS = ()

``CORS_PREFLIGHT_MAX_AGE``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify the number of seconds a client/browser can cache the preflight
response

Note: A preflight request is an extra request that is made when making a
“not-so-simple” request (eg. content-type is not
application/x-www-form-urlencoded) to determine what requests the server
actually accepts. Read more about it here:
http://www.html5rocks.com/en/tutorials/cors/

Default:

::

    CORS_PREFLIGHT_MAX_AGE = 86400

``CORS_ALLOW_CREDENTIALS``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify whether or not cookies are allowed to be included in cross-site
HTTP requests (CORS).

Default:

::

    CORS_ALLOW_CREDENTIALS = False

``CORS_REPLACE_HTTPS_REFERER``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify whether to replace the HTTP\_REFERER header if CORS checks pass
so that CSRF django middleware checks will work with https

Note: With this feature enabled, you also need to add the
corsheaders.middleware.CorsPostCsrfMiddleware after
django.middleware.csrf.CsrfViewMiddleware to undo the header replacement

Default:

::

    CORS_REPLACE_HTTPS_REFERER = False

``CORS_URLS_ALLOW_ALL_REGEX``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify a list of URL regex for which to allow all origins

Example:

::

    CORS_URLS_ALLOW_ALL_REGEX = (r'^/api/users$', )

Default:

::

    CORS_URLS_ALLOW_ALL_REGEX = ()

.. _`https://github.com/ottoyiu/django-cors-headers/`: django-cors-headers%20by%20ottoyiu

.. |Build Status| image:: https://travis-ci.org/zestedesavoir/django-cors-middleware.svg?branch=master
   :target: https://travis-ci.org/zestedesavoir/django-cors-middleware
.. |codecov.io| image:: http://codecov.io/github/zestedesavoir/django-cors-middleware/coverage.svg?branch=master
   :target: http://codecov.io/github/ottoyiu/zestedesavoir/django-cors-middleware?branch=master
.. |PyPI| image:: https://img.shields.io/pypi/v/django-cors-middleware.svg
   :target: https://pypi.python.org/pypi/django-cors-middleware
