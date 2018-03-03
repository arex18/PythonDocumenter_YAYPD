"""
Author: Reuben Ferrante
Date:   27/10/2017
"""

import abc

class ObjectDefinition(abc.ABC):
    ''' Abstract class from which the other classes derive from. It has the basic definitions for getters. '''

    def __init__(self, name, doc_string, parent):
        self.name = name
        self.doc_string = doc_string
        self.parent = parent or ''

    def get_docstring(self):
        return self.doc_string

    # Technically redundant because of __repr__, but may be better for readability. Also, __repr__ might change.
    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def __repr__(self):
        return self.name

class ClassDefinition(ObjectDefinition):
    ''' Derives from  ObjectDefinition. Extends with the necessary getters. '''

    def __init__(self, class_name, function_list : list, class_doc_string='', parent_module=None):
        super().__init__(class_name, class_doc_string, parent_module)
        self.functions = function_list

    def get_functions(self):
        return self.functions

class FunctionDefinition(ObjectDefinition):
    ''' Derives from  ObjectDefinition. Extends with the necessary getters. '''

    def __init__(self, func_name, func_parameters, func_docstring='', parent_module=None):
        super().__init__(func_name, func_docstring, parent_module)
        self.parameters = func_parameters

    def get_parameters(self):
        return self.parameters

class ModuleDefinition(ObjectDefinition):
    ''' Derives from  ObjectDefinition. Extends with the necessary getters. '''

    def __init__(self, module_name, module_docstring, imports, classes, functions, parent_package=None, child=None):
        super().__init__(module_name, module_docstring, parent_package)
        self.classes = classes
        self.functions = functions
        self.child = child
        self.imports = imports

    def get_classes(self):
        return self.classes

    def get_functions(self):
        return self.functions

    def get_child(self):
        return self.child

    def get_imports(self):
        return self.imports

class PackageDefinition(ObjectDefinition):
    ''' Derives from  ObjectDefinition. Extends with the necessary getters. '''

    def __init__(self, package_name = '', modules = None, package_docstring='', parent_library=None):
        super().__init__(package_name, package_docstring, parent_library)
        self.modules = modules or []
        self.sub_packages = {}

    def get_modules(self):
        return self.modules

    def get_subpackages(self):
        return self.sub_packages

    def get_all_variables(self):
        return self.get_name(), self.get_docstring(), self.get_parent(), self.get_modules(), self.get_subpackages()


class LibraryDefinition(ObjectDefinition):
    ''' Derives from  ObjectDefinition. Extends with the necessary getters. Also creates new packages according to
    their tree structure. E.g. if B is a sub-package of A, B will be defined in the sub-packages dict of A. '''

    def __init__(self, library_name = '', packages = None, modules = None, library_docstring='', parent=None):
        super().__init__(library_name, library_docstring, parent)
        self.packages = packages or {}
        self.modules = modules or []

    def get_subpackages(self):
        return self.packages

    def get_modules(self):
        return self.modules

    def create_package(self, package_name, split_char='.'):
        """
        Creates a package inside the correct package structure. Sub packages are handled automatically.
        :param package_name:
        :param split_char: Character used to split between packages and sub-packages, e.g. A-B or A.B.
        :return: created PackageDefinition.
        """
        def _create_package_definition(package_name, parent_library):
            self.packages[package_name] = PackageDefinition(package_name=package_name, parent_library=parent_library)
            return self.packages[package_name]

        if self.packages.get(package_name) != None:
            return self.packages[package_name]
        else:
            # Output files in the same directory structure as the library
            possible_parent_package = split_char.join(package_name.split(split_char)[:-1])
            package = self._get_sub_package(self.packages, package_name, possible_parent_package, split_char)
            if package != None:
                return package
            else:
                return _create_package_definition(package_name=package_name, parent_library=self.name)


    def _get_sub_package(self, package, package_name, parent_package_name, split_char='.'):
        """
        Fetches the correct sub-package from the package hierarchical structure.
        :param package:
        :param package_name:
        :param parent_package_name:
        :param split_char:
        :return: PackageDefinition.
        """
        if package.get(parent_package_name) != None:
            package[parent_package_name].sub_packages[package_name] = PackageDefinition(package_name=package_name, parent_library=parent_package_name)
            return package[parent_package_name].sub_packages[package_name]
        else:
            if parent_package_name == self.name:
                return None
            else:
                temp_package = None
                for i in range(1, 100):
                    temp_package = package.get(split_char.join(parent_package_name.split(split_char)[:-i]))
                    if temp_package != None:
                        break
                if temp_package is None:
                    return None
                else:
                    return self._get_sub_package(temp_package.sub_packages, package_name, parent_package_name, split_char)