import re

from django.conf.urls import url


def _np(name, regex):
    '''Return regex named group.'''
    return '(?P<' + name + '>' + regex + ')'


IDENT_REGEX = r'[A-Za-z0-9_]+'
TYPED_PARAMATER_REGEX = re.compile(''.join([
    r'\\<',
    _np('type_name', IDENT_REGEX),
    r'\\:',
    _np('parameter', IDENT_REGEX),
    r'\\>',
]))
UNTYPED_PARAMETER_REGEX = re.compile(r'\\:' + _np('parameter', IDENT_REGEX))


def _earliest_match(string, *regexes):
    match = None
    for regex in regexes:
        new_match = re.search(regex, string)
        if not new_match:
            continue
        if not match or match.start() > new_match.start():
            match = new_match
    return match


class URLTranslator(object):
    def __init__(self):
        self._mapping_registry = {}

    def register(self, name, regex):
        self._mapping_registry[name] = regex

    def _translate_part(self, parameter, type_name=None):
        if type_name is None:
            return _np(parameter, IDENT_REGEX)

        try:
            return _np(parameter, self._mapping_registry[type_name])
        except KeyError:
            raise ValueError("Unknown regex type: {}".format(type_name))

    def translate(self, route):
        unparsed = re.escape(route)
        chunks = []

        regexes = [TYPED_PARAMATER_REGEX, UNTYPED_PARAMETER_REGEX]
        while True:
            match = _earliest_match(unparsed, *regexes)
            if not match:
                chunks.append(unparsed)
                break
            chunks.append(unparsed[:match.start()])
            chunks.append(self._translate_part(**match.groupdict()))
            unparsed = unparsed[match.end():]

        return ''.join(chunks)

    def url(self, route, view, *args, **kwargs):
        re_route = self.translate(route)
        re_route = '^' + re_route
        if not isinstance(view, (list, tuple)):
            re_route += '$'
        return url(re_route, view, *args, **kwargs)


# Make it easy to use the default translator.
_default_translator = URLTranslator()

simple_url = _default_translator.url
register = _default_translator.register

# Make sure the default translator has some handy defaults.
_default_translator.register('int', '[0-9]+')
