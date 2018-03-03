"""
Author: Reuben Ferrante
Date:   27/10/2017
"""

import re
import logging
import shutil

def strip_file_extension(file_name):
    """
    Takes a file name and strips the file extension.
    :param file_name: str
    :return: file name str without the file extension.
    """
    try:
        temp = str(file_name).split('.')
        if len(temp) > 1:
            return ''.join(temp[:-1])
        else:
            return temp[0]
    except Exception as e:
        logging.ERROR(e)


def substring_occurrences(string, sub_string, include_end=False):
    """
    Returns all indices (start) or (start, end) if include_end = True of a sub_string within a string.
    :param string: String to be searched.
    :param sub_string: Sub string.
    :param include_end: Boolean.
    :return: If  include_end is True, a list of tuples is returned as (start index, end index).
    If False list of start indices.
    """
    return [(a.start(), a.end()) if include_end else a.start() for a in re.finditer(sub_string, string)]


def copy_directory_tree_to_destination(source, destination):
    shutil.copytree(source, destination)