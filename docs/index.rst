.. include:: ../README.rst


Example
=======

The python code of an example application is included entirely here.

.. literalinclude:: ../examples/simple/app.py


In this example, :class:`~flask_diced.Diced` is used directly and required
attributes are passed in when creating an instance of the class, another way is
to subclass and define required attributes as class attributes, as in:

.. code-block:: python

  class UserView(Diced):
      model = User
      create_form_class = CreateUserForm
      edit_form_class = EditUserForm
      delete_form_class = DeleteForm

  user_view = UserView()
  user_view.register(app)


API
===

.. automodule:: flask_diced
  :members:
  :show-inheritance:
  :special-members: __init__


Changelog
=========


Version 0.3
-----------

- Added support to customized view context


Version 0.2
-----------

- Removed test runner dependency in end user installation


Version 0.1
-----------

- Initial public release
