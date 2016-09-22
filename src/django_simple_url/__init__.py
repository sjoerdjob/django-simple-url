import re

from django.conf.urls import url
from django.urls import RegexURLPattern, RegexURLResolver


def _np(name, regex):
    '''Return regex named group.'''
    return '(?P<' + name + '>' + regex + ')'


IDENT_REGEX = r'[A-Za-z0-9_]+'
TYPED_PARAMETER_REGEX = re.compile(''.join([
    r'<',
    _np('type_name', IDENT_REGEX),
    r':',
    _np('parameter', IDENT_REGEX),
    r'>',
]))
UNTYPED_PARAMETER_REGEX = re.compile(r':' + _np('parameter', IDENT_REGEX))


def _earliest_match(string, *regexes):
    match = None
    for regex in regexes:
        new_match = re.search(regex, string)
        if not new_match:
            continue
        if not match or match.start() > new_match.start():
            match = new_match
    return match


class CastingRegexURLPattern(RegexURLPattern):
    def __init__(self, casts, regex, callback, default_args=None, name=None):
        self._casts = casts
        super(CastingRegexURLPattern, self).__init__(regex, callback, default_args, name)

    def resolve(self, path):
        resolvermatch = super(CastingRegexURLPattern, self).resolve(path)
        if resolvermatch:
            kwargs = resolvermatch.kwargs
            for name, caster in self._casts.items():
                if name in kwargs:
                    kwargs[name] = caster(kwargs[name])
        return resolvermatch

class URLTranslator(object):
    def __init__(self):
        self._mapping_registry = {}

    def register(self, name, regex, cast=None):
        self._mapping_registry[name] = (regex, cast)

    def _get_pattern_and_cast(self, type_name=None):
        if type_name is None:
            return r'[A-Za-z0-9_-]+', None

        try:
            return self._mapping_registry[type_name]
        except KeyError:
            raise ValueError("Unknown regex type: {}".format(type_name))

    def translate(self, route):
        unparsed = route
        chunks = []
        casts = {}

        regexes = [TYPED_PARAMETER_REGEX, UNTYPED_PARAMETER_REGEX]
        while True:
            match = _earliest_match(unparsed, *regexes)
            if not match:
                chunks.append(re.escape(unparsed))
                break

            chunks.append(re.escape(unparsed[:match.start()]))

            # Get information.
            groups = match.groupdict()
            parameter = groups['parameter']
            type_name = groups.get('type_name', None)
            pattern, cast = self._get_pattern_and_cast(type_name)
            chunks.append(_np(parameter, pattern))

            if cast is not None:
                casts[parameter] = cast

            unparsed = unparsed[match.end():]

        return ''.join(chunks), casts

    def url(self, route, view, kwargs=None, name=None):
        re_route, casts = self.translate(route)
        re_route = '^' + re_route
        if isinstance(view, (list, tuple)):
            assert not casts, 'casts in include-patterns not supported'
            urlconf_module, app_name, namespace = view
            return RegexURLResolver(re_route, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
        else:
            re_route += '$'
            return CastingRegexURLPattern(casts, re_route, view, kwargs, name)


# Make it easy to use the default translator.
_default_translator = URLTranslator()

simple_url = _default_translator.url
register = _default_translator.register

# Make sure the default translator has some handy defaults.
_default_translator.register('int', '[0-9]+', cast=int)
_default_translator.register('slug', '[A-Za-z0-9_-]+')
