# -*- coding: utf-8 -*-
#
# Flask-Diced documentation build configuration file, created by
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, PROJECT_DIR)
import flask_diced  # noqa

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'

master_doc = 'index'

project = u'Flask-Diced'
copyright = u'2016, Philip Xu'
author = u'Philip Xu'

release = flask_diced.__version__
version = release.rsplit('.', 1)[0]

language = None

exclude_patterns = ['_build']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'
html_theme_options = {
    'github_banner': True,
    'github_repo': 'flask-diced',
    'github_user': 'pyx',
}

htmlhelp_basename = 'Flask-Diceddoc'

latex_documents = [
    (master_doc, 'Flask-Diced.tex', u'Flask-Diced Documentation',
     u'Philip Xu', 'manual'),
]

man_pages = [
    (master_doc, 'flask-diced', u'Flask-Diced Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'Flask-Diced', u'Flask-Diced Documentation',
     author, 'Flask-Diced', 'One line description of project.',
     'Miscellaneous'),
]
