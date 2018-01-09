import re
import os
from tools.shared.module_loader import import_module
from .nested_dict import nested_dict


__all__ = [
    'CodeTemplate', 'IDENT_REGEX', 'YamlLoader', 'nested_dict',
    'split_name_params', 'write',
]


CodeTemplate = import_module('code_template', 'aten/src/ATen/code_template.py').CodeTemplate

try:
    # use faster C loader if available
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader


GENERATED_COMMENT = CodeTemplate("""\
generated from tools/autograd/templates/${filename}""")

# Matches "foo" in "foo, bar" but not "foobar". Used to search for the
# occurence of a parameter in the derivative formula
IDENT_REGEX = r'(^|\W){}($|\W)'


# TODO: Use a real parser here; this will get bamboozled
# by signatures that contain things like std::array<bool, 2> (note the space)
def split_name_params(prototype):
    name, params = re.match('(\w+)\((.*)\)', prototype).groups()
    return name, params.split(', ')


def write(dirname, name, template, env):
    env['generated_comment'] = GENERATED_COMMENT.substitute(filename=name)
    path = os.path.join(dirname, name)
    with open(path, 'w') as f:
        f.write(template.substitute(env))