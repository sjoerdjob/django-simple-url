#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-simple-url',
    version='0.0.4',
    description='Simpler URL specification for Django.',
    author="Sjoerd Job Postmus",
    author_email='sjoerdjob@sjec.nl',
    url='https://github.com/sjoerdjob/django-simple-url',
    packages=['django_simple_url'],
    package_dir={'': 'src'},
    include_package_data=True,
    license='MIT license',
    keywords=['django', 'url'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
