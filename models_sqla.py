#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:55:04 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

import sqlite3
from sqlalchemy import (Column, Integer, String, Boolean, DateTime, JSON,
                        ForeignKey, event)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine


from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_security import AsaList
from sqlalchemy.ext.mutable import MutableList
from flask_security.forms import LoginForm, StringField, Required
from flask_security.utils import lookup_identity

###############################################################################
# Foreign Key Support for SQLite3


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:
        # play well with other database backends
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


###############################################################################
# Create database connection object

db = SQLAlchemy()

###############################################################################
# User Database Models

DEFAULT_SETTING = {
    'display_name': '',
    'theme': 'united',
}


class Role(db.Model, RoleMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    level = Column(Integer)
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean, default=True)
    fs_uniquifier = Column(String(255), unique=True)
    confirmed_at = Column(DateTime)
    settings = Column(JSON, default=DEFAULT_SETTING)
    last_login_at = Column(DateTime)
    current_login_at = Column(DateTime)
    last_login_ip = Column(String(255))
    current_login_ip = Column(String(255))
    login_count = Column(Integer)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    role_id = Column('role_id', Integer, ForeignKey('role.id'))


###############################################################################
# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

###############################################################################


class CustomLoginForm(LoginForm):
    email = StringField('Username or Email', validators=[Required()])

    def validate(self, **kwargs) -> bool:
        self.user = lookup_identity(self.email.data)
        if self.user is None:
            self.email.errors = ["Invalid username or email"]
            return False

        self.ifield = self.email
        # NOTE: setting username data is a temporary solution for a bug which
        # might be fixed in the later versions of Flask-Security-Too
        # Ref: https://github.com/Flask-Middleware/flask-security/issues/732
        self.username.data = self.user.username
        return super().validate(**kwargs)


###############################################################################
