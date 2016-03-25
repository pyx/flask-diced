# -*- coding: utf-8 -*-
import re
from os import path
from setuptools import setup

ROOT_DIR = path.abspath(path.dirname(__file__))

DESCRIPTION = 'Flask-Diced - CRUD views generator for Flask'
LONG_DESCRIPTION = open(path.join(ROOT_DIR, 'README.rst')).read()
VERSION = re.search(
    "__version__ = '([^']+)'",
    open(path.join(ROOT_DIR, 'flask_diced.py')).read()
).group(1)


setup(
    name='Flask-Diced',
    version=VERSION,
    url='https://github.com/pyx/flask-diced/',
    license='BSD-New',
    author='Philip Xu',
    author_email='pyx@xrefactor.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    py_modules=['flask_diced'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest>=2.8.2',
        'Flask-SQLAlchemy',
        'Flask-WTF',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
