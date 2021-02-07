#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:59:16 2020

@author: Hrishikesh Terdalkar
"""

###############################################################################

from flask_security import UserMixin, RoleMixin, MongoEngineUserDatastore
from flask_security.forms import LoginForm, RegisterForm, StringField, Required
from flask_mongoengine import MongoEngine

###############################################################################

# Create database connection object
db = MongoEngine()

###############################################################################


class Settings(db.EmbeddedDocument):
    display_name = db.StringField(max_length=30, default='')
    theme = db.StringField(max_length=20, default='united')


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    level = db.IntField()
    permissions = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    username = db.StringField(max_length=255, unique=True)
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    fs_uniquifier = db.StringField(max_length=255)
    confirmed_at = db.DateTimeField()
    settings = db.EmbeddedDocumentField(Settings, default=Settings())
    roles = db.ListField(db.ReferenceField(Role), default=['member'])


###############################################################################
# Setup Flask-Security

user_datastore = MongoEngineUserDatastore(db, User, Role)

###############################################################################


class CustomRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])


class CustomLoginForm(LoginForm):
    email = StringField('Username or Email', [Required()])

###############################################################################
