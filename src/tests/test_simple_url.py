from django.test import SimpleTestCase
from django.urls import RegexURLPattern

from django_simple_url import simple_url


class SimpleURLTests(SimpleTestCase):
    def test_parameter_free_url(self):
        def stub_view(): pass
        pattern = simple_url('/hello/world/', stub_view)

        self.assertIsInstance(pattern, RegexURLPattern)
        
        match = pattern.resolve('/hello/world/')
        self.assertIsNot(match, None)
        self.assertIs(match.func, stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {})

    def test_parameter_simple_parameters(self):
        def stub_view(): pass
        pattern = simple_url('/:year/:month/', stub_view)

        self.assertIsInstance(pattern, RegexURLPattern)
        
        match = pattern.resolve('/2003/02/')
        self.assertIsNot(match, None)
        self.assertIs(match.func, stub_view)
        self.assertEqual(match.args, ())
        self.assertEqual(match.kwargs, {
            'year': '2003',
            'month': '02',
        })
