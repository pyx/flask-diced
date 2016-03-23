============================================
Flask-Diced - CRUD views generator for Flask
============================================

Flask-Diced is a set of helper classes for `Flask`_ that generates CRUD views
and registers them to blueprint/application.

Flask-Diced provides:

- **D**\ etail view
- **I**\ ndex view
- **C**\ reate view
- **E**\ dit view
- **D**\ elete view


.. _Flask: http://flask.pocoo.org/


Flask-Diced Might Not Be What You Want
======================================

Flask-Diced is opinionated, it assumes:

- the model object has a :code:`save` method for data persistence and
  :code:`delete` method to remove itself.
- the model can be created with no required arguments.
- the form used for creation and editing are in the style of `Flask-WTF`_'s,
  specifically, Flask-Diced expects the form accepts a named parameter
  :code:`obj` to pass in the initial value for editing as well as
  :code:`validate_on_submit` method and :code:`populate_obj` method on the form
  class.  In short, just use `Flask-WTF`.
- the client should be redirected when done for POST requests.
- views should have minimal business logic.


.. _Flask-WTF: https://pypi.python.org/pypi/Flask-WTF


Flask-Diced is Extensible
=========================

Flask-Diced is designed in a way that customizations can be easily done.  All
properties and methods can be overridden for customization.

Flask-Diced can be customized to the point that the assumptions described in
last section are refer to the default implementation and will no longer hold
true if you customize relevant parts of it.

e.g.,

*Want to change how the objects list is fetched?*

  Override :code:`query_all`

*Want to change the name of endpoint of the edit view?*

  Redefine :code:`edit_endpoint`

*Want to use your own view function or control how views are registered?*

  Override respective view/register methods.


Installation
============

Flask-Diced is on PyPI.

.. code-block:: sh

  pip install Flask-Diced


License
=======

BSD New, see LICENSE for details.


Links
=====

- `Documentation <http://flask-diced.readthedocs.org/>`_

- `Issue Tracker <https://github.com/pyx/flask-diced/issues/>`_

- `Source Package @ PyPI <https://pypi.python.org/pypi/Flask-Diced/>`_

- `Mercurial Repository @ bitbucket
  <https://bitbucket.org/pyx/flask-diced/>`_

- `Git Repository @ Github
  <https://github.com/pyx/flask-diced/>`_

- `Git Repository @ Gitlab
  <https://gitlab.com/pyx/flask-diced/>`_

- `Development Version
  <http://github.com/pyx/flask-diced/zipball/master#egg=Flask-diced-dev>`_
