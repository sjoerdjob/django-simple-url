django-simple-url
=================

django-simple-url allows developers to specify Django routes without having to
learn the complicated intricacies of regular expressions, and is meant as a
drop-in replacement of the native Django ``url`` function.

Usage
-----

Using django-simple-url is almost the same as using the native Django ``url``
function.

.. code-block:: python

    # main/urls.py
    from django_simple_url import simple_url

    from . import views

    urlpatterns = [
        simple_url('', views.index),
        simple_url('posts/<int:id>/', views.post),
    ]

It also works nicely with other apps, like for instance the Django Admin.

.. code-block:: python

    # main/urls.py
    from django.contrib import admin
    from django_simple_url import simple_url

    urlpatterns = [
        simple_url('admin/', admin.site.urls),
    ]

Allowed formats
---------------

The following methods are allowed to specify the route.

Flask-like syntax
'''''''''''''''''

The most complete definition is as follows:

.. code-block:: python

    simple_url(r'posts/<int:year>/<int:month>/', views.post_list)

Converter-free syntax
'''''''''''''''''''''

This is similar to the Flask-like syntax, except that it does not explicitly
specify the type. In this case, the type defaults to ``slug``.

.. code-block:: python
    simple_url(r'posts/<year>/<month>/', views.post_list)

Rails-like syntax (Deprecated)
''''''''''''''''''''''''''''''

This is the easiest syntax, but for simplicity of implementation will eventually
be gone.

.. code-block:: python

    simple_url(r'posts/:year/:month/', views.posts_list)

Inspiration
-----------

The development of this library is inspired by the following post on the Django
mailing list: `Challenge teaching Django to beginners: urls.py <https://groups.google.com/forum/#!topic/django-developers/u6sQax3sjO4>`_.

