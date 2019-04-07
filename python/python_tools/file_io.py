"""
file_io.py

Description:
    Tools and utilities for operating on files or file like objects
"""
# stdlib
import json
import os
import sys


# ==============================================================================
# general
# ==============================================================================
def get_home_dir():
    """
    Returns the full file path of the current user's home directory

    :return: the current user's home directory
    :rtype: str
    """
    if "win" in sys.platform:
        home = os.getenv("HOMEPATH")
    if "linux" in sys.platform:
        home = os.getenv("HOME")
    if "darwin" in sys.platform:
        home = os.getenv("HOME")
    return os.path.abspath(home)


def line_processor(filepath, func, *func_args, **func_kwargs):
    """
    Runs each line in the given filepath through the specified function

    :param filepath: full path to the file you wish to operate on
    :type filepath: str
    :param func: callable object used to process each line
    :type func: any callable
    :param *func_args: miscellaneous positional parameters to the callable
    :type *func_args: tuple
    :param **func_kwargs: miscellaneous keywork parameters to the callable
    :type **func_kwargs: dict
    :return: n/a
    :rtype: n/a
    """
    for line in open(filepath, 'r'):
        func(line, *args, **kwargs)


# ==============================================================================
# diff
# ==============================================================================
def are_equal(file_a, file_b):
    """
    Compares 2 files to see if their contents are the same

    :param file_a: full path to the first file
    :type file_a: str
    :param file_b: The file to check against
    :type file_b: str
    :return: if the 2 files match
    :rtype: bool
    """
    for a_line in open(file_a, 'r'):
        for b_line in open(file_b, 'r'):
            if a_line != b_line:
                return False
    return True


# ==============================================================================
# json
# ==============================================================================
def write_json(filepath, data, overwrite=False):
    """
    Writes or appends the given data to the specified filepath

    :param filepath: full path to the .json file
    :type filepath: str        
    :param data: the data to add
    :type data: dict
    :param overwrite: option to overwrite existing data
    :type overwrite: bool
    :return: The full path name of the json file
    :rtype: str
    """
    # merge data - if necessary
    if not overwrite and os.path.isfile(filepath):
        with open(filepath, 'r') as infile:
            current_data = json.load(infile)
            data.update(current_data)

    # write file
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return filepath
