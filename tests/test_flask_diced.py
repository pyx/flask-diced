# -*- coding: utf-8 -*-
# NOTE: to run the tests, please get development source code with examples
import os
import sys

from flask import url_for

import pytest


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'examples', 'simple'))

from app import User, app as example_app, db  # noqa


USERNAME = 'John Doe'
EMAIL = 'john@example.com'


@pytest.yield_fixture(autouse=True)
def app():
    example_app.config['TESTING'] = True
    example_app.config['WTF_CSRF_ENABLED'] = False
    ctx = example_app.test_request_context()
    ctx.push()
    db.create_all()

    yield example_app

    db.drop_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user():
    john = User(username=USERNAME, email=EMAIL)
    john.save()
    return john


def test_detail_view(app, user):
    with app.test_client() as client:
        response = client.get(url_for('detail', pk=user.id))
        html = response.data.decode()
        assert USERNAME in html
        assert EMAIL in html


def test_index_view(app, user):
    with app.test_client() as client:
        response = client.get(url_for('index'))
        html = response.data.decode()
        assert USERNAME in html
        assert EMAIL in html


def test_create_view(app):
    with app.test_client() as client:
        response = client.post(
            url_for('create'),
            follow_redirects=True,
            data=dict(username=USERNAME, email=EMAIL))
        html = response.data.decode()
        assert 'user created' in html

    john = User.query.one()
    assert john.username == USERNAME
    assert john.email == EMAIL


def test_create_view_with_get_should_fail(app):
    with app.test_client() as client:
        response = client.get(
            url_for('create'),
            follow_redirects=True,
            query_string=dict(username=USERNAME, email=EMAIL))
        html = response.data.decode()
        assert 'user created' not in html

    assert User.query.count() == 0


def test_edit_view(app, user):
    with app.test_client() as client:
        response = client.post(
            url_for('edit', pk=user.id),
            follow_redirects=True,
            data=dict(username='Jane Doe', email='jane@example.com'))
        html = response.data.decode()
        assert 'user updated' in html

    jane = User.query.one()
    assert jane.username == 'Jane Doe'
    assert jane.email == 'jane@example.com'


def test_edit_view_with_get_should_fail(app, user):
    with app.test_client() as client:
        response = client.get(
            url_for('edit', pk=user.id),
            follow_redirects=True,
            query_string=dict(username='Jane Doe', email='jane@example.com'))
        html = response.data.decode()
        assert 'user updated' not in html

    john = User.query.one()
    assert john.username == USERNAME
    assert john.email == EMAIL


def test_delete_view(app, user):
    with app.test_client() as client:
        response = client.post(
            url_for('delete', pk=user.id),
            follow_redirects=True)
        html = response.data.decode()
        assert 'user deleted' in html

    assert User.query.count() == 0


def test_delete_view_with_get_should_fail(app, user):
    with app.test_client() as client:
        response = client.get(
            url_for('delete', pk=user.id),
            follow_redirects=True)
        html = response.data.decode()
        assert 'user deleted' not in html

    john = User.query.one()
    assert john.username == USERNAME
    assert john.email == EMAIL
