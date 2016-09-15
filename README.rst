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
        url('admin/', admin.site.urls),
    ]

Caveats
-------

It should be noted that even though the type ``int`` appears in the syntax
``<int:post_id>``, the value passed to the view is still a string. The ``int``
part of the syntax only limits the URLs that are matched, but does not alter
the value passed to the view.

Inspiration
-----------

The development of this library is inspired by the following post on the Django
mailing list: `Challenge teaching Django to beginners: urls.py <https://groups.google.com/forum/#!topic/django-developers/u6sQax3sjO4>`_.

