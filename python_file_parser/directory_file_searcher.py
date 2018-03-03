"""
Author: Reuben Ferrante
Date:   27/10/2017
"""

import os
import logging

class DirectorySearcher():
    """
    Searches the directory for .py files.
    """


    @classmethod
    def get_directory_tree(cls, path : str, delimiter : str= '\\'):
        """
        Walks the entire directory and returns a dictionary.
        :param path: Absolute path to search in.
        :param delimiter: Path delimiter to split by.
        :return: dictionary of key = package + filename, value = [absolute path, None, None, None]
        """

        logging.debug("Searching directory")
        files = {}
        main_package_name = path.split(delimiter)[-1]
        FIRST_RUN_FLAG = True
        module_names = None
        naked_files = None

        for (dirpath, dirnames, filenames) in os.walk(path):
            if FIRST_RUN_FLAG:
                module_names = dirnames
                if '__pycache__' in module_names:
                    module_names.remove('__pycache__')
                naked_files = filenames
                FIRST_RUN_FLAG = False

            if "pycache" in dirpath:
                continue
            package_name = str.replace(dirpath[dirpath.find(main_package_name):], delimiter, '.')
            files.update(cls._get_directory_files(filenames=filenames,
                                                  path=dirpath,
                                                  delimiter=delimiter,
                                                  package_name=package_name))
        return files, module_names, naked_files

    @staticmethod
    def _get_directory_files(filenames : list, path : str, delimiter : str, package_name : str):
        """
        Gets all the files in a directory.
        :param filenames:
        :param path:
        :param delimiter:
        :param package_name:
        :return: files dict, where key = package_name.file, value = [package_name, None, path, None, None, None]
        """
        files = {}
        for file in filenames:
            if ".py" in file:
                # Add package name, package description, dir, modules, functions
                # (description, modules, classes, functions are None until they are updated)
                files[package_name +
                             '.' +
                             file[:-3]] = [package_name, None, ''.join([path, delimiter, file]), None, None, None]
        return files