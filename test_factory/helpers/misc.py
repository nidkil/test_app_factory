"""
This module contains miscellaneous convenience helper functions.
"""
import errno
import operator
import os

OUTPUT_PRINT = 'print'
OUTPUT_LIST = 'list'
OUTPUT_STRING = 'string'


def pretty_print_config(config, indent=0, output_format=OUTPUT_PRINT):
    """
    Takes a Flask config, orders the config and creates a readable format for debugging purposes. It supports
    nested configurations by calling its self recursively. The output method can be specified: print, list or
    string.

    Parameters
    ----------
    config: config
        The config to pretty print.
    indent: int
        Number of tabs to indent.
    output_format: string
        The output format.

    Returns
    -------
    string, list
        Returns the ordered config in the specified format.
    """

    result = []
    # First sort the configuration so that the keys are in alphabetical order.
    sorted_d = sorted(config.iteritems(), key=operator.itemgetter(0))
    for key, value in sorted_d:
        indent_str = '\t' * indent
        if isinstance(value, dict):
            line = '{}{:40s}'.format(indent_str, key)
            pretty_print_config(value, indent + 1, output_format)
        else:
            line = '{}{:40s}{}'.format(indent_str, key, value)
        result.append(line)
    if output_format == OUTPUT_PRINT:
        for line in result:
            print line
    elif output_format == OUTPUT_LIST:
        return result
    else:
        s = ''
        for line in result:
            if len(s) > 0:
                s += '\n'
            s += line
        return s


def get_root_path(path, name_root_folder='src'):
    """
    Determines the root directory of the project. It helps when running files that are not in the root directory,
    like running test files directly.

    Parameters
    ----------
    path: string
        The fully qualified path of the path to determine the root directory from.
    name_root_folder: string
        The name of the root directory folder.

    Returns
    -------
    string
        Returns the path to the root directory.
    """

    test_for = name_root_folder
    if not test_for.startswith(os.sep):
        test_for = os.sep + test_for
    if not test_for.endswith(os.sep):
        test_for += os.sep

    pos = path.find(test_for)
    if pos > 0:
        return path[:pos + 4]
    raise ValueError('The path does not contain a subdirectory named \'{}\' [{}]'.format(name_root_folder, path))


def create_path(path):
    """
    Checks if a directory exists, if it doesn't it is created.

    Parameters
    ----------
    path: string
        The fully qualified path of the directory to check.
    """

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
