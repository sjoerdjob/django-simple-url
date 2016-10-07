from abc import abstractmethod


class BaseConverter(object):
    """
    URL parameter converter.
    """
    regex = None

    @abstractmethod
    def to_python(self, value):
        pass

    @abstractmethod
    def to_url(self, value):
        pass

    def get_regex(self):
        return self.regex


class IntConverter(BaseConverter):
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


class SlugConverter(BaseConverter):
    regex = '[A-Za-z0-9_-]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class StrConverter(BaseConverter):
    regex = '[^/]+'  # Everything except a '/'.

    def to_python(self, value):
        return value

    def to_url(self, value):
        if '/' in value:
            raise ValueError(
                "Can't reverse {:r}, it contains a slash".format(value)
            )
        return value


class OldStyleConverter(BaseConverter):
    def __init__(self, regex, to_python):
        self.regex = regex
        self.transform = to_python

    def to_python(self, value):
        return self.transform(value)

    def to_value(self, value):
        return value
