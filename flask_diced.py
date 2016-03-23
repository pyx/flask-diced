# -*- coding: utf-8 -*-
"""Flask-Diced - CRUD views generator for Flask"""

from flask import flash, redirect, render_template, url_for


__version__ = '0.2.dev0'

__all__ = [
    'Detail', 'Index', 'Create', 'Edit', 'Delete',
    'Base', 'Diced',
    'persistence_methods',
]


def apply_decorators(func, decorators):
    for decorator in reversed(decorators):
        func = decorator(func)
    return func


def persistence_methods(datastore):
    """class decorator that adds persistence methods to the model class

    :param datastore:
        SQLAlchemy style datastore, should sopport
        :code:`datastore.session.add()`, :code:`datastore.session.delete()`
        and :code:`datastore.session.commit()` for model persistence.

    Two persistence methods will be added to the decorated class

    :data:`save(self, commit=True)`
        the save method

    :data:`delete(self, commit=True)`
        the delete method
    """
    def class_decorator(cls):
        def save(self, commit=True):
            datastore.session.add(self)
            if commit:
                datastore.session.commit()

        def delete(self, commit=True):
            datastore.session.delete(self)
            if commit:
                datastore.session.commit()

        cls.save = save
        cls.delete = delete
        return cls
    return class_decorator


class Detail(object):
    """detail view mixin"""

    #: decorators to be applied to detail view
    detail_decorators = ()

    #: the endpoint for the detail view URL rule
    detail_endpoint = 'detail'

    #: the URL rule for the detail view
    detail_rule = '/<int:pk>/'

    @property
    def detail_template(self):
        """default template name for detail view

        generated with :attr:`~Base.object_name` and :attr:`detail_endpoint`
        """
        return '{}/{}.html'.format(self.object_name, self.detail_endpoint)

    def detail_view(self, pk):
        """detail view function

        :param pk:
            the primary key of the model to be shown.
        """
        context = {self.object_name: self.query_object(pk)}
        return render_template(self.detail_template, **context)

    def register_detail_view(self, blueprint):
        """register detail view to blueprint

        :param blueprint:
            the Flask Blueprint or Application object to which the detail view
            will be registered.
        """
        view = apply_decorators(self.detail_view, self.detail_decorators)
        blueprint.add_url_rule(self.detail_rule, self.detail_endpoint, view)


class Index(object):
    """index view mixin"""

    #: decorators to be applied to index view
    index_decorators = ()

    #: the endpoint for the index view URL rule
    index_endpoint = 'index'

    #: the URL rule for the index view
    index_rule = '/'

    @property
    def index_template(self):
        """default template name for index view

        generated with :attr:`~Base.object_name` and :attr:`index_endpoint`
        """
        return '{}/{}.html'.format(self.object_name, self.index_endpoint)

    def index_view(self):
        """index view function"""
        context = {self.object_list_name: self.query_all()}
        return render_template(self.index_template, **context)

    def register_index_view(self, blueprint):
        """register index view to blueprint

        :param blueprint:
            the Flask Blueprint or Application object to which the index view
            will be registered.
        """
        view = apply_decorators(self.index_view, self.index_decorators)
        blueprint.add_url_rule(self.index_rule, self.index_endpoint, view)


class Create(object):
    """create view mixin"""

    #: decorators to be applied to create view
    create_decorators = ()

    #: the endpoint for the create view URL rule
    create_endpoint = 'create'

    #: the message to be flashed for the next request when done
    create_flash_message = None

    #: the form class for new object, with Flask-WFT compatible API
    create_form_class = None

    #: the name for variable representing the form in template
    create_form_name = 'form'

    #: the name of view to redirect the client to when done
    create_redirect_to_view = '.index'

    #: the URL rule for the create view
    create_rule = '/create/'

    @property
    def create_redirect_url(self):
        """the url the client will be redirected to when done

        the default value is the url of :attr:`create_redirect_to_view`
        """
        return url_for(self.create_redirect_to_view)

    @property
    def create_template(self):
        """default template name for create view

        generated with :attr:`~Base.object_name` and :attr:`create_endpoint`
        """
        return '{}/{}.html'.format(self.object_name, self.create_endpoint)

    def create_view(self):
        """create view function"""
        form = self.create_form_class()
        if form.validate_on_submit():
            obj = self.model()
            form.populate_obj(obj)
            obj.save()
            message = self.create_flash_message
            if message is None:
                message = self.object_name + ' created'
            if message:
                flash(message)
            return redirect(self.create_redirect_url)
        context = {self.create_form_name: form}
        return render_template(self.create_template, **context)

    def register_create_view(self, blueprint):
        """register create view to blueprint

        :param blueprint:
            the Flask Blueprint or Application object to which the create view
            will be registered.
        """
        view = apply_decorators(self.create_view, self.create_decorators)
        blueprint.add_url_rule(
            self.create_rule, self.create_endpoint, view,
            methods=['GET', 'POST'])


class Edit(object):
    """edit view mixin"""

    #: decorators to be applied to edit view
    edit_decorators = ()

    #: the endpoint for the edit view URL rule
    edit_endpoint = 'edit'

    #: the message to be flashed for the next request when done
    edit_flash_message = None

    #: the form class for editing object, with Flask-WFT compatible API
    edit_form_class = None

    #: the name for variable representing the form in template
    edit_form_name = 'form'

    #: the name of view to redirect the client to when done
    edit_redirect_to_view = '.index'

    #: the URL rule for the edit view
    edit_rule = '/<int:pk>/edit/'

    @property
    def edit_redirect_url(self):
        """the url the client will be redirected to when done

        the default value is the url of :attr:`edit_redirect_to_view`
        """
        return url_for(self.edit_redirect_to_view)

    @property
    def edit_template(self):
        """default template name for edit view

        generated with :attr:`~Base.object_name` and :attr:`edit_endpoint`
        """
        return '{}/{}.html'.format(self.object_name, self.edit_endpoint)

    def edit_view(self, pk):
        """edit view function

        :param pk:
            the primary key of the model to be edited.
        """
        obj = self.query_object(pk)
        form = self.edit_form_class(obj=obj)
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            message = self.edit_flash_message
            if message is None:
                message = self.object_name + ' updated'
            if message:
                flash(message)
            return redirect(self.edit_redirect_url)
        context = {self.edit_form_name: form}
        return render_template(self.edit_template, **context)

    def register_edit_view(self, blueprint):
        """register edit view to blueprint

        :param blueprint:
            the Flask Blueprint or Application object to which the edit view
            will be registered.
        """
        view = apply_decorators(self.edit_view, self.edit_decorators)
        blueprint.add_url_rule(
            self.edit_rule, self.edit_endpoint, view, methods=['GET', 'POST'])


class Delete(object):
    """delete view mixin"""

    #: decorators to be applied to delete view
    delete_decorators = ()

    #: the endpoint for the delete view URL rule
    delete_endpoint = 'delete'

    #: the message to be flashed for the next request when done
    delete_flash_message = None

    #: the form class for deletion confirmation, should validate if confirmed
    delete_form_class = None

    #: the name for variable representing the form in template
    delete_form_name = 'form'

    #: the name of view to redirect the client to when done
    delete_redirect_to_view = '.index'

    #: the URL rule for the delete view
    delete_rule = '/<int:pk>/delete/'

    @property
    def delete_redirect_url(self):
        """the url the client will be redirected to when done

        the default value is the url of :attr:`delete_redirect_to_view`
        """
        return url_for(self.delete_redirect_to_view)

    @property
    def delete_template(self):
        """default template name for delete view

        generated with :attr:`~Base.object_name` and :attr:`delete_endpoint`
        """
        return '{}/{}.html'.format(self.object_name, self.delete_endpoint)

    def delete_view(self, pk):
        """delete view function

        :param pk:
            the primary key of the model to be deleted.
        """
        obj = self.query_object(pk)
        form = self.delete_form_class(obj=obj)
        if form.validate_on_submit():
            obj.delete()
            message = self.delete_flash_message
            if message is None:
                message = self.object_name + ' deleted'
            if message:
                flash(message)
            return redirect(self.delete_redirect_url)
        context = {self.delete_form_name: form}
        return render_template(self.delete_template, **context)

    def register_delete_view(self, blueprint):
        """register delete view to blueprint

        :param blueprint:
            the Flask Blueprint or Application object to which the delete view
            will be registered.
        """
        view = apply_decorators(self.delete_view, self.delete_decorators)
        blueprint.add_url_rule(
            self.delete_rule, self.delete_endpoint, view,
            methods=['GET', 'POST'])


class Base(object):
    """base class with properties and methods used by mixins"""

    #: views that will be registered when :meth:`register` is called
    views = {'detail', 'index', 'create', 'edit', 'delete'}

    #: views that will not be registered when :meth:`register` is called, even
    #: if they are also listed in :attr:`views`
    exclude_views = set()

    #: the model class
    model = None

    @property
    def object_list_name(self):
        """default name for variable representing list of objects in templates

        generated with :attr:`object_name` in detault implementation.
        """
        return self.object_name + '_list'

    @property
    def object_name(self):
        """default name for variable representing object in templates

        generated with the name of model class in detault implementation.
        """
        return getattr(self.model, '__name__', 'object').lower()

    def __init__(self, **options):
        """create an instance of view generator

        all keyword arguments passed in will be set as the instance's
        attribute if the name is not starting with '_'
        """
        self.__dict__.update(
            (k, v) for (k, v) in options.items() if not k.startswith('__'))

    def query_object(self, pk):
        """returns the object with matching :code:`pk`"""
        return self.model.query.get_or_404(pk)

    def query_all(self):
        """returns all objects"""
        return self.model.query.all()

    def register(self, blueprint):
        """register all enabled views to the :code:`blueprint`

        :param blueprint:
            the Flask Blueprint or Application object to which enalbed views
            will be registered.
        """
        for name in set(self.views) - set(self.exclude_views):
            getattr(self, '_'.join(['register', name, 'view']))(blueprint)


class Diced(Detail, Index, Create, Edit, Delete, Base):
    """CRUD views generator"""
