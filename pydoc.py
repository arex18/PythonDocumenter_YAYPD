"""
Author: Reuben Ferrante
Date:   27/10/2017
"""

from html_utils.py_html_processor import HTMLCreator
from python_file_parser.file_parser import FileParser
from pydocumenter_utils.type_definitions import *
from pydocumenter_utils.pydoc_utils import *
import os
import logging
import argparse
import re

format = dict(format='%(asctime)s - %(message)s\t', datefmt='%d/%m/%Y %I:%M:%S %p')
logger = logging.getLogger()

logging.basicConfig(level=logging.INFO, **format)
logger.setLevel(logging.INFO)


def get_content(parser, path: str, split_char='-', delimiter=os.sep):
    """
    Walks the entire directory and returns a LibraryDefinition with the correct parent-child hierarchical
    package structure.
    :param path: Absolute path to search in.
    :param split_char: File name delimiter to split by.
    :return: LibraryDefinition
    """

    logging.debug("Searching directory")
    library_name = path.split(delimiter)[-1]

    main_library = None
    for (dirpath, dirnames, filenames) in os.walk(path):

        library_name_end_index = substring_occurrences(dirpath, library_name, include_end=True)[0][-1] + len(delimiter)
        parent_name = str.replace(dirpath[library_name_end_index:], delimiter, split_char)

        if "pycache" in dirpath:
            continue

        if parent_name == library_name or parent_name == '':
            main_library = LibraryDefinition(library_name=str.replace(dirpath[dirpath.find(library_name):], delimiter, split_char))
            package = main_library
        else:
            package = main_library.create_package(package_name=parent_name, split_char=split_char)

        package_description = ''
        modules_list = []
        for file in filenames:
            if ".py" in file:
                directory = ''.join([dirpath, delimiter, file])
                imports = parser.find_imports(directory)
                classes, functions, module_description, temp_package_description = parser.find_classes_and_functions(
                    directory)
                classes.sort(key=lambda x: x.get_name())
                functions.sort(key=lambda x: x.get_name())
                if temp_package_description is not '':
                    package_description = ''.join([package_description, temp_package_description])
                modules_list.append(
                    ModuleDefinition(file, module_description, imports, classes, functions, parent_name))
        package.modules = modules_list
        package.doc_string = package_description

    return main_library

def get_correct_path(path):
    path = os.path.join(*re.split('//|/|\\\\', path)).strip()
    if ':' in path:
        i = path.find(':')
        if path[:i+2] != os.sep:
            path = os.path.join(path[:i+1], os.sep, path[i+1:])
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YAYPD! Yet Another Python Documenter')
    parser.add_argument('-i', '--library_path', type=str,
                        help = 'Python project/package/module path, e.g. C:/MyProject')
    parser.add_argument('-o', '--output_path', type=str,
                        help='Path where to output the docs. Folder doesn\'t need to exist.')
    parser.add_argument('-c', '--split_char', type=str,
                        help='Separation character to add to the output folder\'s name to'
                              'represent a directory structure, e.g. MyProject/blog/main.py'
                              ' --> blog-main.html',
                        default='-')
    args = parser.parse_args()

    logger.info("Parsing library: {}".format(args.library_path))
    logger.info("Generating Documentation in: {}".format(args.output_path))
    logger.info("File separator: {}".format(args.split_char))

    # Checks for path errors
    args.library_path = get_correct_path(args.library_path)
    args.output_path = get_correct_path(args.output_path)

    assert isinstance(args.library_path, str)
    assert isinstance(args.output_path, str)
    assert os.path.isdir(args.library_path)

    # Start parsing
    parser = FileParser()
    library = get_content(parser, args.library_path, split_char=args.split_char)

    html_creator = HTMLCreator(args.output_path, library, split_char=args.split_char).create_html_doc()
