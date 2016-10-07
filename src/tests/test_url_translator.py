from unittest import expectedFailure
from django.test import SimpleTestCase

from django_simple_url import URLTranslator
from django_simple_url.converters import (
    IntConverter,
    OldStyleConverter,
    SlugConverter,
    StrConverter,
)


class _EqualOnInstance(object):
    def __init__(self, class_to_check):
        self._class_to_check = class_to_check

    def __eq__(self, other):
        return isinstance(other, self._class_to_check)


class URLTranslatorTests(SimpleTestCase):
    def setUp(self):
        self.translator = URLTranslator()

    def test_url_translator_maps_normal_url_to_url(self):
        self.assertEqual(
            self.translator.translate('hello/world/'),
            (r'hello\/world\/', {}),
        )

    def test_url_translator_escapes_regex_special_characters(self):
        self.assertEqual(
            self.translator.translate('hello.world/'),
            (r'hello\.world\/', {}),
        )

    def test_url_translator_maps_parameters_to_patterns(self):
        self.assertEqual(
            self.translator.translate(':year/'),
            (r'(?P<year>[^/]+)\/', {
                'year': _EqualOnInstance(StrConverter),
            }),
        )

    def test_registering_without_cast(self):
        self.translator.register('foo_int', r'[0-9]+')
        self.assertEqual(
            self.translator.translate('<foo_int:year>/'),
            (r'(?P<year>[0-9]+)\/', {
                'year': _EqualOnInstance(OldStyleConverter),
            }),
        )

    def test_registering_with_cast(self):
        self.translator.register('foo_int', r'[0-9]+', int)
        self.assertEqual(
            self.translator.translate('<foo_int:year>/'),
            (r'(?P<year>[0-9]+)\/', {
                'year': _EqualOnInstance(OldStyleConverter),
            }),
        )

    def test_parameters_between_angled_brackets(self):
        self.assertEqual(
            self.translator.translate('<year>/'),
            (r'(?P<year>[^/]+)\/', {
                'year': _EqualOnInstance(StrConverter),
            }),
        )
