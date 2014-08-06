# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import codecs
from functools import wraps
import os


def parse_md_file(file_name):
    """Return the YAML and MD sections."""
    in_yaml = False
    yaml_lines = []
    md_lines = []
    with codecs.open(file_name, encoding='utf8') as fh:
        for line in fh:
            if line.strip() == '---':
                in_yaml = not in_yaml

            if in_yaml:
                yaml_lines.append(line)
            else:
                md_lines.append(line)

    return ''.join(yaml_lines), ''.join(md_lines)


def chdir(dirname=None):
    """Decorator to run a function in a different directory then return."""
    def decorator(func):

        @wraps(func)
        def inner(*args, **kwargs):
            curdir = os.getcwd()
            try:
                if dirname is not None:
                    os.chdir(dirname)
                return func(*args, **kwargs)
            finally:
                os.chdir(curdir)

        return inner

    return decorator
