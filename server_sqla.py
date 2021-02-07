#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:28:31 2020

@author: Hrishikesh Terdalkar
"""

###############################################################################

import os
import glob
import json

import git
import requests
from flask import (Flask, render_template, request, redirect, flash,
                   session, Response)
from flask_security import (Security, auth_required, roles_required,
                            hash_password, current_user, user_registered,
                            user_authenticated)
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate

from models_sqla import db, user_datastore, CustomLoginForm, CustomRegisterForm
from settings import app
import constants

###############################################################################

CONSTANTS = vars(constants)

###############################################################################
# Flask Application

webapp = Flask(app.name)
webapp.config['DEBUG'] = True

webapp.config['SECRET_KEY'] = app.secret_key
webapp.config['SECURITY_PASSWORD_SALT'] = app.security_password_salt
webapp.config['JSON_AS_ASCII'] = False

# SQLAlchemy Config
webapp.config['SQLALCHEMY_DATABASE_URI'] = app.sqla['database_uri']
webapp.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
}

# CSRF Token Expiry
webapp.config['WTF_CSRF_TIME_LIMIT'] = None

###############################################################################
# Flask-Security-Too Configuration

webapp.config['SECURITY_REGISTERABLE'] = True
webapp.config['SECURITY_SEND_REGISTER_EMAIL'] = app.smtp_enabled
webapp.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ['email', 'username']
webapp.config['SECURITY_RECOVERABLE'] = app.smtp_enabled
webapp.config['SECURITY_CHANGEABLE'] = True
webapp.config['SECURITY_TRACKABLE'] = True

###############################################################################
# Mail Configuration

if app.smtp_enabled:
    webapp.config['MAIL_SERVER'] = app.smtp['server']
    webapp.config['MAIL_USERNAME'] = app.smtp['username']
    webapp.config['MAIL_DEFAULT_SENDER'] = (app.smtp['name'],
                                            app.smtp['username'])
    webapp.config['MAIL_PASSWORD'] = app.smtp['password']
    webapp.config['MAIL_USE_SSL'] = app.smtp['use_ssl']
    webapp.config['MAIL_USE_TLS'] = app.smtp['use_tls']
    webapp.config['MAIL_PORT'] = app.smtp['port']

###############################################################################
# Initialize standard Flask extensions

db.init_app(webapp)

csrf = CSRFProtect(webapp)
security = Security(webapp, user_datastore,
                    login_form=CustomLoginForm,
                    register_form=CustomRegisterForm)
mail = Mail(webapp)
migrate = Migrate(webapp, db)

###############################################################################
# Hooks


@webapp.before_first_request
def init_database():
    """Initiate database and create adminn user"""
    db.create_all()
    app.roles = {}
    for role_definition in app.role_definitions:
        name = role_definition['name']
        description = role_definition['description']
        permissions = role_definition['permissions']
        level = role_definition['level']
        role = user_datastore.find_or_create_role(
            name=name,
            description=description,
            level=level,
            permissions=permissions
        )
        app.roles[name] = role

    if not user_datastore.find_user(username=app.admin['username']):
        user_datastore.create_user(
            username=app.admin['username'],
            email=app.admin['email'],
            password=hash_password(app.admin['password']),
            roles=[app.roles['owner'], app.roles['admin'], app.roles['member']]
        )
    db.session.commit()


@user_registered.connect_via(webapp)
def assign_default_roles(sender, user, **extra):
    """Assign member role to users after successful registration"""
    user_datastore.add_role_to_user(user, app.roles['member'])
    db.session.commit()


@user_authenticated.connect_via(webapp)
def _after_authentication_hook(sender, user, **extra):
    pass

###############################################################################


@webapp.route("/")
@auth_required()
def show_home():
    data = {}
    data['title'] = 'Home'
    return render_template('home.html', data=data, constants=CONSTANTS)


@webapp.route("/admin", strict_slashes=False)
@roles_required('admin')
@auth_required()
def show_admin():
    data = {}
    data['title'] = 'Admin'
    data['roles'] = [role.name for role in current_user.roles]
    return render_template('admin.html', data=data, constants=CONSTANTS)


@webapp.route("/settings", strict_slashes=False)
@auth_required()
def show_settings():
    theme_files = glob.glob(
        os.path.join(app.dir, 'static', 'themes', 'css', 'bootstrap.*.min.css')
    )
    print(app.dir, theme_files)
    themes = sorted([os.path.basename(theme).split('.')[1]
                     for theme in theme_files])

    data = {}
    data['title'] = 'Settings'
    data['themes'] = ['default'] + themes

    return render_template('settings.html', data=data, constants=CONSTANTS)


@webapp.route("/action", methods=["POST"], strict_slashes=False)
@auth_required()
def action():
    try:
        action = request.form['action']
    except KeyError:
        flash("Insufficient paremeters in request.")
        return redirect(request.referrer)

    # ----------------------------------------------------------------------- #
    # Admin Actions

    owner_actions = [
        'application_info', 'application_update', 'application_reload'
    ]

    admin_actions = [
        'update_user_role'
    ]

    if action in owner_actions and not current_user.has_role('owner'):
        flash("You are not authorized to perform that action.", "danger")
        return redirect(request.referrer)

    if action in admin_actions and not current_user.has_role('admin'):
        flash("You are not authorized to perform that action.", "danger")
        return redirect(request.referrer)

    # ----------------------------------------------------------------------- #
    # Show Application Information
    if action in [
        'application_info', 'application_update', 'application_reload'
    ] and not app.pa_enabled:
        flash("PythonAnywhere configuration incomplete or missing.")
        return redirect(request.referrer)

    if action == 'application_info':
        info_url = app.pa_api_url + app.pa_api_actions['info']
        response = requests.get(info_url, headers=app.pa_headers)
        if response.status_code == 200:
            pretty_info = json.dumps(
                json.loads(response.content.decode()),
                indent=2
            )
            session['admin_result'] = pretty_info
        else:
            print(response.content.decode())
            flash("Something went wrong.")
        return redirect(request.referrer)

    # Perform git-pull
    if action == 'application_update':
        try:
            repo = git.cmd.Git(app.dir)
            result = repo.pull()
        except Exception as e:
            result = f'Error\n{e}'
        session['admin_result'] = result

        if result == 'Already up-to-date.':
            flash("Already up-to-date.")
        elif 'Updating' in result and 'changed,' in result:
            flash("Application code has been updated.", "success")
        else:
            flash("Something went wrong.")
        return redirect(request.referrer)

    # API App Reload
    if action == 'application_reload':
        reload_url = app.pa_api_url + app.api_actions['reload']
        response = requests.post(reload_url, headers=app.pa_headers)
        if response.status_code == 200:
            flash("Application has been reloaded.", "success")
            return Response("Success")
        else:
            print(response.content.decode())
            flash("Something went wrong.")
            return Response("Failure")

    # ----------------------------------------------------------------------- #
    # Manage User Role

    if action == 'update_user_role':
        target_user = request.form['target_user']
        target_role = request.form['target_role']

        _user = user_datastore.find_user(username=target_user)
        _role = app.roles[target_role]

        user_level = max([role.level for role in current_user.roles])
        target_level = max([role.level for role in _user.roles])
        if _user == current_user:
            flash("You cannot modify your own role.")
        elif user_level <= target_level:
            flash(f"You cannot modify role '{target_role}'.", "danger")
        else:
            user_datastore.add_role_to_user(_user, _role)
            flash(f"Updated role of user '{target_user}' to '{target_role}'.")
        return redirect(request.referrer)

    # ----------------------------------------------------------------------- #
    # Update Settings

    if action == 'update_settings':
        display_name = request.form['display_name']
        theme = request.form['theme']

        settings = {
            'display_name': display_name,
            'theme': theme
        }
        current_user.settings = settings
        db.session.commit()
        return redirect(request.referrer)

    # ----------------------------------------------------------------------- #
    # Action Template

    if action == 'custom_action':
        # action code
        status = True  # action_result
        if status:
            flash("Action completed successfully.", "success")

    # ----------------------------------------------------------------------- #

    if not status:
        flash("Action failed.", "danger")

    return redirect(request.referrer)

###############################################################################


if __name__ == '__main__':
    import socket

    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = '5025'

    webapp.run(host=host, port=port, debug=True)
