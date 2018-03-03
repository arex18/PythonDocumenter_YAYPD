"""
Author: Reuben Ferrante
Date:   27/10/2017
"""

import ast
from pydocumenter_utils.type_definitions import *
from python_file_parser.filetags import *
import re
import logging

class FileParser():

    def find_imports(self, directory):
        """
        Find all imports that are used in a .py file.
        :param directory: file path.
        :return: list of imports.
        """
        with open(directory, 'r') as f:
            imports = self.__find_modules(f)
            if imports:
                return sorted(list(imports))
            else:
                return imports

    def find_classes_and_functions(self, directory):
        """
        Parses all classes and functions and builds ClassDefinitions and FunctionDefinitions lists.
        :param directory: str pointing to the .py file directory
        :return: lists classes, functions, module_description, package_description
        """
        classes, functions, module_description, package_description = [], [], '', ''
        try:
            with open(directory, 'r') as f:
                classes, functions, module_description, package_description = self._find_classes_and_functions(f)
        except Exception as e:
            print("Could not process file {0}. Error: {1}".format(directory, e))
        return classes, functions, module_description, package_description

   
    def get_modules_and_functions_in_py_files_and_update_dict(self, directory_tree : dict):
        """
        Iterates over directory tree and finds modules in each file.
        :param directory_tree: dictionary where key = filename, val = absolute directory
        :return: updated dictionary with val = (directory : str, modules : set)
        """

        logging.info("Parsing Directory")
        package_description = ''

        for (key, (package_name, _, directory, _, _, _)) in directory_tree.items():

            logging.info("Key: {}".format(key))
            try:
                file_object = open(directory, 'r')
                with open(directory, 'r') as f:
                    modules = self.__find_modules(f)

                    logging.info("Finding Classes and Functions in {}".format(directory))
                    classes, functions, file_description, temp_package_description = self._find_classes_and_functions(f)

                    if temp_package_description is not None:
                        package_description = ''.join([package_description, temp_package_description])
                    # This can be moved outside. Left here not to iterate twice over dict.
                    directory_tree[key] = [package_name, file_description, directory, modules, classes, functions]
            except Exception as e:
                print("Error in get_modules_and_functions_in_py_files_and_update_dict, key = {0}. Error {1}".format(
                    key, e))

        return directory_tree, package_description

  
    def _find_classes_and_functions(self, file_content):
        """
        Finds functions found with keywords "def"
        :param directory: string giving the absolute directory of the py file.
        :return: set containing all the modules for a given file.
        """

        classes = []
        functions = []
        module_description = ''
        next_class_descriptor = ''
        package_description = ''

        p = ast.parse(file_content.read())
        for obj in p.body:
            if isinstance(obj, ast.Expr):
                if hasattr(obj.value, 's'):
                    if FILE_DESCRIPTOR in obj.value.s:
                        module_description = re.sub(r': ', '', str.replace(obj.value.s, FILE_DESCRIPTOR, ''))
                    elif CLASS_DESCRIPTOR in obj.value.s:
                        next_class_descriptor = re.sub(r': ', '', str.replace(obj.value.s, CLASS_DESCRIPTOR, ''))
                    elif PACKAGE_DESCRIPTOR in obj.value.s:
                        package_description = re.sub(r': ', '', str.replace(obj.value.s, PACKAGE_DESCRIPTOR, ''))

            elif isinstance(obj, ast.ClassDef):
                # temp_class_functions, class_description = self.__get_class_definition(obj, next_class_descriptor)
                # classes.append(ClassDefinition(obj.name, temp_class_functions, class_description))
                classes.append(ClassDefinition(obj.name, *self.__get_class_functions_and_description(obj, next_class_descriptor)))
                next_class_descriptor = ''

            elif isinstance(obj, ast.FunctionDef):
                functions.append(self.__get_function_definition(obj))
                next_class_descriptor = ''

        return classes, functions, module_description, package_description

  
    def __get_class_functions_and_description(self, obj, next_class_descriptor):
        """
        Parses a "ast" class definition, goes through all functions.
        :param obj: Object in .py parser body, e.g. class ast.
        :param next_class_descriptor: Class description.
        :return: function list, class description str
        """
        class_functions = []
        for funcdef in obj.body:
            if isinstance(funcdef, ast.FunctionDef):
                class_functions.append(self.__get_function_definition(funcdef))

        if next_class_descriptor is not '':
            class_description = next_class_descriptor + ast.get_docstring(obj)
        else:
            class_description = ast.get_docstring(obj)

        return class_functions, class_description

 
    def __get_function_definition(self, func):
        """
        Uses "ast" library to get the parameters, docstring, and create a FunctionDefinition
        as defined in type_definidtions.py
        :param func: ast.FunctionDef instance
        :return: FunctionDefinition(...)
        """
        parameters = self.__get_function_parameters(func)
        docstring = ast.get_docstring(func)
        return FunctionDefinition(func_name=func.name, func_parameters=parameters, func_docstring = docstring)

    @staticmethod
    def __get_function_parameters(funcdef):
        """
        Get the parameters from a function parsed using the "ast" library
        :param funcdef: FunctionDef as defined in "ast"
        :return: parameter str list.
        """
        parameters = []
        if hasattr(funcdef, 'args'):
            for arg_obj in funcdef.args.args:
                if arg_obj.annotation is None:
                    parameters.append(arg_obj.arg)
                else:
                    parameters.append(''.join([arg_obj.arg, ' : ', arg_obj.annotation.id]))
        return parameters

    @staticmethod
    def __find_modules(file_content):
        """
        Finds modules found with keywords "import" and "from"  in .py files and returns a set()
        :param directory: string giving the absolute directory of the py file.
        :return: set containing all the modules for a given file.
        """
        modules = set()

        try:
            for line in file_content:
                if "import " in line:
                    split_line = line.split()
                    split_line = [str.replace(split_line[i], ',', '') for i, mod in enumerate(split_line)]
                    if 'as' in split_line:
                        split_line[split_line.index('as'):] = []
                    if "from" in line:
                        main_mod = split_line[1]
                        modules.update(''.join([main_mod, '.', sub_mod]) for sub_mod in split_line[3:])
                    else:
                        modules.update(mod for mod in split_line[1:])
        except Exception as e:
            logging.ERROR("Error in __find_modules: %s", e)
        finally:
            if (len(modules) == 0):
                return None
            else:
                return modules
