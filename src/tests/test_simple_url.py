from django.test import SimpleTestCase
from django.conf.urls import include
from django.urls import RegexURLPattern

from django_simple_url import simple_url


class SimpleURLTests(SimpleTestCase):
    def test_parameter_free_url(self):
        def stub_view(): pass
        resolver = simple_url('hello/world/', stub_view)

        match = resolver.resolve('hello/world/')
        self.assertIs(match.func, stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {})

    def test_parameter_simple_parameters(self):
        def stub_view(): pass
        resolver = simple_url(':year/:month/', stub_view)

        match = resolver.resolve('2003/02/')
        self.assertIs(match.func, stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {
            'year': '2003',
            'month': '02',
        })

    def test_parameter_typed_parameters(self):
        def stub_view(): pass
        resolver = simple_url('<int:year>/<int:month>/', stub_view)

        match = resolver.resolve('2003/02/')
        self.assertIs(match.func, stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {
            'year': '2003',
            'month': '02',
        })

    def test_anchoring_with_simple_view(self):
        def stub_view(): pass
        resolver = simple_url('hello/world/', stub_view)

        self.assertIsNone(resolver.resolve('prefix/hello/world/'))
        self.assertIsNone(resolver.resolve('hello/world/suffix/'))

    def test_anchoring_included_views(self):
        def stub_posts_index_view(): pass
        def stub_posts_item_view(): pass
        class stub_module:
            urlpatterns = [
                simple_url('', stub_posts_index_view),
                simple_url(':post_id/', stub_posts_item_view),
            ]

        resolver = simple_url('posts/', include(stub_module))

        match = resolver.resolve('posts/')
        self.assertIs(match.func, stub_posts_index_view)

        match = resolver.resolve('posts/123/')
        self.assertIs(match.func, stub_posts_item_view)
        self.assertEqual(match.kwargs, {'post_id': '123'})
