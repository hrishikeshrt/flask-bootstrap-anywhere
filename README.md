# Flask-Bootstrap-Anywhere

This is a skeleton application written in python using Flask microframework.
It comes with support for user registration, login, session management,
password recovery, password reset and database connection.
These features are achieved by `Flask-Security-Too`, which in turn achieves
them by various flask extensions such as `Flask-Login`, `Flask-WTF` etc.
Front-end styling is done using `Bootstrap`.

## Motivation

In general, many web applications require some level of user-management.
While `Django` can be suitable for big projects, for relatively small projects
it might be an overkill. Further, `Flask` offers more flexibility.
However, with `Flask` being a "microframework", we have to choose from a variety
of plugins to build a working system.

This application fits together a handful of such commonly used plugins
for commonly required tasks, and aims to save developers' effort.

## Features

### Back-end

* User Management
    * Registration
    * Login
    * Session Management
    * Password Recovery
    * Roles
* Database Support
    * MySQL
    * SQLite
    * MongoDB (incomplete)
* Mail
* Migrations (Powered by `Flask-Migrate`)
* Deployment
    * Support for Git-powered release on on `PythonAnywhere`

### Front-end

* `Bootstrap`-powered clean front-end
* Elegant themes powered by https://bootswatch.com/
* Ability to change themes on the fly
* Sample Front-end Components (TODO)

## Requirements

* For package requirements, check `requirements.txt`
* Mail functionality requires SMTP access.
* For `PythonAnywhere` deployment, an account on https://www.pythonanywhere.com/ is required.
    * `PythonAnywhere` free accounts do not support non-HTTP(S) ports, this results in
       `MongoDB`, `
* MySQL access required if MySQL is used as backend server.

## Setup

Getting started with the basic application is straightforward.

* Install the requirements from the `requirements.txt`,

```console
$ pip3 install -r requirements.txt
```

* Copy `settings.sample.py` to `settings.py` and update it as required.

Most of the settings can also be specified through environment variables.
There are inline explanations in the settings file if the variables are not self-explanatory.

## Run

Run the application using,

````console
$ python server.py
````

OR

```
$ export FLASK_APP="server:webapp"
$ flask run
```

(Other WSGI-based deployments are also possible. e.g. `gunicorn`)

### Database Support

By default, SQLite3 database will be used. To use MySQL, update credentials
either through `settings.py` or through environment variables.
In `settings.py`, set `USE_SQLITE` to `False` and `USE_MYSQL` to `True`.

Support for PostgreSQL, although not explicitly added, is easy to figure out.
It can be achieved in a similar manner to MySQL support by installing the necessary driver
and using the proper `database_uri` for `SQLAlchemy`.

MongoDB support may be added in the future, although it's not too difficult to figure it out.

### Mail

If SMTP credentials are added, mail support will be enabled. This would enable password recovery
by receiving a link for password reset, as well as a welcome mail after registration.

Contents of these emails can be modified by editing templates in `tempaltes/security/email`

### PythonAnywhere Support

* Create a free account on https://www.pythonanywhere.com/
* Generate a token
* Clone your repository on the server
* Set-up your application by setting propery WSGI paths
* Once your application is running, for future updates, you can use "Update" and "Reload" buttons from `Admin` tab to update your application.
* For `PythonAnywhere` free accounts, only SMTP permitted is `smtp.gmail.com`.

## Contribute

Aim of this project is to provide a basic skeleton for development of simple, beautiful and functional web applications.

Feel free to contribute towards that end by,

* Providing new features
* Improving current features
* Improving code quality
* Adding documentation

## License

GNU GPL v3
