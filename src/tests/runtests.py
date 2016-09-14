#!/usr/bin/env python
import os
import sys

import django
import django.conf


def main():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))

    django.conf.settings.configure()
    django.setup()
    arguments = list(sys.argv)
    arguments.insert(1, 'test')
    django.core.management.execute_from_command_line(arguments)


if __name__ == '__main__':
    main()
