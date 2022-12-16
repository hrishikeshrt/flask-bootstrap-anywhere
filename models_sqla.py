#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 19:55:04 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, JSON,
                        ForeignKey)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, AsaList
from flask_security.forms import LoginForm, RegisterForm, StringField, Required

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


class CustomRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])

    def validate(self):
        if user_datastore.find_user(username=self.username.data):
            self.username.errors = ["Username already taken"]
            return False

        if not super(CustomRegisterForm, self).validate():
            return False

        return True


class CustomLoginForm(LoginForm):
    email = StringField('Username or Email', [Required()])

###############################################################################
