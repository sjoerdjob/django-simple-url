import re

from django.conf.urls import url

PARAMETER_REGEX = re.compile(r'\\:(?P<parameter>[A-Za-z0-9_]+)')


class URLTranslator(object):
    def translate(self, route):
        re_route = re.escape(route)
        re_route = PARAMETER_REGEX.sub(r'(?P<\1>[A-Za-z0-9_]+)', re_route)
        return re_route


def simple_url(route, view, *args, **kwargs):
    re_route = URLTranslator().translate(route)
    re_route = '^' + re_route
    if not isinstance(view, (list, tuple)):
        re_route += '$'
    return url(re_route, view, *args, **kwargs)
