from django.test import SimpleTestCase, override_settings
from django.conf.urls import include
from django.urls import resolve, reverse, Resolver404

from django_simple_url import simple_url


def _stub_view(): pass
def _stub_posts_index_view(): pass
def _stub_posts_item_view(): pass


class SimpleURLTests(SimpleTestCase):
    @override_settings(ROOT_URLCONF=[
        simple_url('hello/world/', _stub_view),
    ])
    def test_parameter_free_url(self):
        match = resolve('/hello/world/')
        self.assertIs(match.func, _stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {})

    @override_settings(ROOT_URLCONF=[
        simple_url(':year/:month/', _stub_view),
    ])
    def test_parameter_simple_parameters(self):
        match = resolve('/2003/02/')
        self.assertIs(match.func, _stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {
            'year': '2003',
            'month': '02',
        })

    @override_settings(ROOT_URLCONF=[
        simple_url('<int:year>/<int:month>/', _stub_view),
    ])
    def test_parameter_typed_parameters(self):
        match = resolve('/2003/02/')
        self.assertIs(match.func, _stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {
            'year': 2003,
            'month': 2,
        })

    @override_settings(ROOT_URLCONF=[
        simple_url('hello/world/', _stub_view),
    ])
    def test_anchoring_with_simple_view(self):
        with self.assertRaises(Resolver404):
            self.assertIsNone(resolve('/prefix/hello/world/'))
        with self.assertRaises(Resolver404):
            self.assertIsNone(resolve('/hello/world/suffix/'))

    @override_settings(ROOT_URLCONF=[
        simple_url('posts/', include([
            simple_url('', _stub_posts_index_view),
            simple_url(':post_id/', _stub_posts_item_view),
        ])),
    ])
    def test_anchoring_included_views(self):
        match = resolve('/posts/')
        self.assertIs(match.func, _stub_posts_index_view)

        match = resolve('/posts/123/')
        self.assertIs(match.func, _stub_posts_item_view)
        self.assertEqual(match.kwargs, {'post_id': '123'})
