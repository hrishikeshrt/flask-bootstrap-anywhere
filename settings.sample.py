#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:06:12 2020

@author: Hrishikesh Terdalkar
"""

###############################################################################

import os
from configuration import Configuration

###############################################################################

DEBUG = False

APP_NAME = "MyFlaskWebApp"
APP_TITLE = "MyHeader"
APP_YEAR = "2020"
APP_AUTHOR = "Hrishikesh Terdalkar"

APP_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_FILE = os.path.join(APP_DIR, "flask.log")

# DB_DIR is used for specifying directory containing SQLite3 database

DB_DIR = "db"
DATA_DIR = "data"

# --------------------------------------------------------------------------- #

APPLICATION_CONFIG = {}

# --------------------------------------------------------------------------- #
# Security

# Generate a nice key using secrets.token_urlsafe()
SECRET_KEY = os.environ.get("SECRET_KEY", "Secret Key for Flask Webapp")

# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
SECURITY_PASSWORD_SALT = os.environ.get(
    "SECURITY_PASSWORD_SALT", "301721846670564486948773381866193921949"
)

# --------------------------------------------------------------------------- #
# First User

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "admin")
ADMIN_MAIL = os.environ.get("ADMIN_MAIL", "admin@127.0.0.1")

# --------------------------------------------------------------------------- #
# PythonAnywhere

PA_DOMAIN = os.environ.get("PA_DOMAIN", "")
PA_USERNAME = os.environ.get("PA_USERNAME", "")
PA_TOKEN = os.environ.get("PA_TOKEN", "")

# --------------------------------------------------------------------------- #
# SMTP Config

SMTP_ENABLED = False

SMTP_SENDER_NAME = os.environ.get("SMTP_SENDER_NAME", "")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_PORT = os.environ.get("SMTP_PORT", "587")
SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "0")
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "1")

# --------------------------------------------------------------------------- #
# MongoDB Config

MONGO_HOST = os.environ.get("MONGO_HOST", "")
MONGO_USER = os.environ.get("MONGO_USER", "")
MONGO_PASS = os.environ.get("MONGO_PASS", "")
MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "")
MONGO_OPTIONS = os.environ.get("MONGO_OPTIONS", "")

# --------------------------------------------------------------------------- #
# MySQL Config

MYSQL_USER = os.environ.get("MYSQL_USER", "")
MYSQL_PASS = os.environ.get("MYSQL_PASS", "")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "")

# --------------------------------------------------------------------------- #
# SQLite Config

SQLITE_DATABASE = os.environ.get("SQLITE_DATABASE", "test.db")

# --------------------------------------------------------------------------- #

USE_MONGO = False
USE_MYSQL = False
USE_SQLITE = True

# --------------------------------------------------------------------------- #
# Role Definitions

ROLES = [
    {
        "name": "guest",
        "level": 1,
        "description": "Guest",
        "permissions": []
    },
    {
        "name": "member",
        "level": 5,
        "description": "Member",
        "permissions": ["view_ucp"]
    },
    {
        "name": "admin",
        "level": 100,
        "description": "Administrator",
        "permissions": ["view_acp", "add_admin"]
    },
    {
        "name": "owner",
        "level": 1000,
        "description": "Owner",
        "permissions": ["view_acp", "remove_admin"]
    },
]

###############################################################################
# DO NOT EDIT

app = Configuration()
app.name = APP_NAME
app.title = APP_TITLE
app.author = APP_AUTHOR
app.year = APP_YEAR

app.debug = DEBUG

# Config
app.config = APPLICATION_CONFIG

# Paths
app.dir = APP_DIR
app.db_dir = os.path.join(APP_DIR, DB_DIR)
app.data_dir = os.path.join(APP_DIR, DATA_DIR)

app.log_file = LOG_FILE

# Security

app.secret_key = SECRET_KEY
app.security_password_salt = SECURITY_PASSWORD_SALT

# Users

app.admin = {
    "username": ADMIN_USER,
    "email": ADMIN_MAIL,
    "password": ADMIN_PASS
}

app.role_definitions = ROLES

# PythonAnywhere
# https://help.pythonanywhere.com/pages/API

app.pa_enabled = bool(PA_DOMAIN and PA_USERNAME and PA_TOKEN)
app.pa_api_actions = {
    "info": f"/webapps/{PA_DOMAIN}/",
    "reload": f"/webapps/{PA_DOMAIN}/reload/",
}

app.pa_api_url = f"https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/"
app.pa_headers = {
    "Authorization": f"Token {PA_TOKEN}"
}

# MongoDB

if USE_MONGO:
    app.mongo = {
        "host": (f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/"
                 f"{MONGO_DATABASE}?retryWrites=true&w=majority"),
        "connect": False,
        "connectTimeoutMS": 30000,
        "socketTimeoutMS": None,
        "socketKeepAlive": True,
        "maxPoolsize": 1
    }

# SMTP

app.smtp_enabled = SMTP_ENABLED
app.smtp = {
    "name": SMTP_SENDER_NAME,
    "server": SMTP_SERVER,
    "username": SMTP_USER,
    "password": SMTP_PASS,
    "port": int(SMTP_PORT),
    "use_ssl": bool(int(SMTP_USE_SSL)),
    "use_tls": bool(int(SMTP_USE_TLS))
}


# MySQL

if USE_MYSQL:
    app.sqla = {
        "database_uri": (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}"
            f"@{MYSQL_HOST}/{MYSQL_DATABASE}"
        )
    }

# SQLite

if USE_SQLITE:
    app.sqla = {
        "database_uri": (
            f"sqlite:///{os.path.join(app.db_dir, SQLITE_DATABASE)}"
        )
    }

###############################################################################
