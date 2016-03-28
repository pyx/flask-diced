#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, ValidationError

from flask_diced import Diced, persistence_methods


app = Flask(__name__)

# Need this for WTForm CSRF protection
app.config['SECRET_KEY'] = 'no one knows'

# Need this for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

db = SQLAlchemy(app)


# persistence_methods is a class decorator that adds save and delete methods
@persistence_methods(db)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)


def unique(model, column, message='already exists'):
    def unique_validator(form, field):
        obj = model.query.filter(column == field.data).first()
        if obj and obj.id != form._obj_id:
            raise ValidationError(message)
    return unique_validator


class UserForm(Form):
    username = TextField('Username',
                         [DataRequired(), unique(User, User.username)])
    email = EmailField('Email',
                       [DataRequired(), Email(), unique(User, User.email)])

    def __init__(self, **kwargs):
        super(UserForm, self).__init__(**kwargs)
        self._obj_id = kwargs['obj'].id if 'obj' in kwargs else None


class CreateUserForm(UserForm):
    submit = SubmitField('Create')


class EditUserForm(UserForm):
    submit = SubmitField('Update')


class DeleteForm(Form):
    submit = SubmitField('Delete')


# view decorator that does nothing, for showing how to add decorators to views
def no_op_decorator(view):
    return view


# create a view generator for User model, these two arguments for decorators
# are here for demonstration purpose and are not mandatory
user_view = Diced(
    model=User,
    create_form_class=CreateUserForm,
    edit_form_class=EditUserForm,
    delete_form_class=DeleteForm,
    index_decorators=[no_op_decorator],
    edit_decorators=[no_op_decorator, no_op_decorator],
)


# Register on application directly, works on Blueprint as well
user_view.register(app)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
