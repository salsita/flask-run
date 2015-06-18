# [Flask-Run](https://github.com/salsita/flask-run) <a href='https://github.com/salsita'><img align='right' title='Salsita' src='https://www.google.com/a/cpanel/salsitasoft.com/images/logo.gif?alpha=1' /></a>

Flask-based web application runner.

[![Latest Version](https://pypip.in/version/Flask-Run/badge.svg)]
(https://pypi.python.org/pypi/Flask-Run/)
[![Downloads](https://pypip.in/download/Flask-Run/badge.svg)]
(https://pypi.python.org/pypi/Flask-Run/)
[![Supported Python versions](https://pypip.in/py_versions/Flask-Run/badge.svg)]
(https://pypi.python.org/pypi/Flask-Run/)
[![License](https://pypip.in/license/Flask-Run/badge.svg)]
(https://pypi.python.org/pypi/Flask-Run/)


## Supported Platforms

* [Python](http://www.python.org/) >= 2.7, 3.3
* [Flask](http://flask.pocoo.org/) >= 0.9


## Get Started

Install using [pip](https://pip.pypa.io/) or [easy_install](http://pythonhosted.org/setuptools/easy_install.html):
```bash
pip install Flask-Run
easy_install Flask-Run
```

## Example:

#### Flask application: `app.py`

```python
#!/usr/bin/env python

"""Flask-based web application."""

__all__ = 'app'.split()

import flask
from config import Config

app = None

def create_app(config=Config):
  app = flask.Flask(__name__)

  app.config.from_object(config)

  return app

if __name__ == '__main__':
    from flask.ext.run import run
    run(create_app, Config)
```

#### Flask configuration: `config.py`

See [sample flask configuration `config.py](https://github.com/salsita/flask-config#flask-configuration-configpy)
from [flask-config package](https://github.com/salsita/flask-config)
that supports listing and selecting environment configurations.

#### Usage:

```
usage: app.py [-h] [-b [HOST|:PORT]] [-r] [-R] [-d] [-D] [-e ENV]
              [-E [SHOW_ENV]] [-g]

runs Flask-based web application using Python WSGI reference server

optional arguments:
  -h, --help            show this help message and exit
  -b [HOST|:PORT], --bind [HOST|:PORT]
                        bind to HOST:PORT (default: 127.0.0.1:5000)
  -r, --reload          reload server on code change (default in development)
  -R, --no-reload       do not reload server on code change
  -d, --debug           show debugger on exception (default in development)
  -D, --no-debug        do not show debugger on exception
  -e ENV, --env ENV     select environment config (default: development)
  -E [SHOW_ENV], --show-env [SHOW_ENV]
                        show environment config and exit (*: all, default: development)
  -g, --gen-key         generate a good secret key and exit

optional environment variables:
  APP_ENV               select environment configuration
  DATABASE_URL          sqlalchemy database uri including credentials
  SECRET_KEY            secret key for signing session cookies

available environment configurations (*: active):
* dev | development
  prod | production
  qa | test | testing
  stage | staging
  try | experimental

```

## Changelog

### 0.1.3

#### Fixes

- Fix package setup on Python 3.

### 0.1.2

#### Fixes

- Fix package setup to not require dependencies preinstalled.

### 0.1.0

#### Features

* Initial release.
