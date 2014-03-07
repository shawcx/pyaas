pyaas
-----

PyaaS, or pyaas, or Python-as-a-Service, is a simple wrapper around `Tornado <http://www.tornadoweb.org/>`_ that makes it quick and easy to rapid deploy new web applications. It has a settings parser, storage engine, and authentication modules.

Usage
-----

::

    # install pyaas
    pip install pyaas

    # seed an example project in the named directory
    python -m pyaas.skel --name example

    # start the seed project
    python example/example.py

The site is now available at http://localhost:8080/

Edit the file ``example/etc/example.ini`` to tweak the configuration of the server.

Hosted at `GitHub <https://github.com/moertle/pyaas>`_ and `PyPi <https://pypi.python.org/pypi/pyaas>`_

People using pyaas:

- `deploy.tk <http://github.com/moertle/deploy.tk>`_
