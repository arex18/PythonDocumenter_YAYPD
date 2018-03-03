"""
Author: Reuben Ferrante
Date:   27/10/2017
"""

from jinja2 import Environment, FileSystemLoader
from pydocumenter_utils.pydoc_utils import *
import os

MODULE_FILE_DIR = 'templates/module.html'
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_FILE_DIR = 'templates/package.html'
LIBRARY_STRUCTURE = 'templates/library_structure.html'


class HTMLCreator():
    """
    This class contains all the processing of packages and modules as well as generation of html files.
    It is where all files are created and documentation is parsed. It recursively walks a library and
    outputs the html documentation in the same format as the python package folder structure.
    """

    def __init__(self, save_directory : str, library=None, directory_delimiter ='\\', split_char='-'):
        logging.debug("Created HTML Creator")
        self.directory_delimiter = directory_delimiter
        self.j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                                  trim_blocks=True,
                                  lstrip_blocks=True)
        self.j2_env.filters['strip_file_extension'] = strip_file_extension
        self.j2_env.globals['css_directory'] = save_directory.replace(self.directory_delimiter, '/')
        self.j2_env.globals['library_title'] = str(library)

        self.split_char = split_char
        self.library = library
        self.save_directory = save_directory

    def set_library(self, library):
        """ Setter for library. """
        self.library = library

    def create_html_doc(self):
        """
        Main caller after all the Python files are processed by the file parser.
        The folder structure is created and the package is processed. The process is
        recursive, recycling code...
        :return:
        """
        dir = self._create_directory(self.directory_delimiter.join([self.save_directory, str(self.library)]))
        self.process_package(self.library, dir)
        try:
            copy_directory_tree_to_destination('html_utils\\static', self.save_directory + '\\static')
        except FileExistsError as e:
            logging.info("CSS files already exist.")
        except Exception as e:
            print("Error when copying CSS files to directory. Error: {0}".format(e))

    def process_module(self, module, save_directory, html_directory_link, package):
        """
        Called during package processing. Processes the module in a similar way by calling
        the correct template, generating the relative links and saving the template in the
        correct folder.
        :param module:
        :param save_directory:
        :param html_directory_link:
        :param package:
        :return: Nothing.
        """
        #parent_directory_link = self._get_module_html_and_parent_llink(package)
        navigation_template, main_library_link, css_link = self._create_library_navigation_template(package, module=module)

        classes = module.get_classes()
        doc_string = module.get_docstring()
        name = module.get_name()
        parent = module.get_parent()
        imports = module.get_imports()
        functions = module.get_functions()

        template = self.j2_env.get_template(MODULE_FILE_DIR).render(
            file_title=name,
            parent=parent,
            doc_string=doc_string,
            imports=imports,
            functions=functions,
            classes=classes,
            library_structure=navigation_template,
            author_name='Reuben Ferrante',
            directory_link=html_directory_link,
            parent_directory_link='../'+str(parent),
            main_library_link=main_library_link + str(self.library),
            css_link=css_link
        )
        self._save_template_to_html(save_directory, name, template)

    def process_package(self, package, save_directory):
        """
        A recursive function that goes through an entire package and documents its modules.
        All templates are subsequently called from the respective module/package.
        :param package: Package type.
        :param save_directory: Directory for the project to be saved in.
        :return: Nothing.
        """
        main_package_dir = self._create_directory(self.directory_delimiter.join([save_directory, str(package).split('.')[-1]]))
        parent = None
        try:
            parent = package.get_parent()
        except Exception as e:
            print("Error: Package {} has no parent.".format(str(package)))

        html_directory_link, parent_directory_link = self._get_package_html_and_parent_link(package, main_package_dir)
        navigation_template, main_library_link, css_link = self._create_library_navigation_template(package)

        sub_packages = package.get_subpackages()
        for _, sub_package in iter(sub_packages.items()):
            self.process_package(sub_package, main_package_dir)

        p_modules = package.get_modules()
        for module in p_modules:
            self.process_module(module, main_package_dir, html_directory_link, package)

        p_name = package.get_name()

        template = self.j2_env.get_template(PACKAGE_FILE_DIR).render(
            file_title=p_name,
            modules=p_modules,
            sub_packages=package.get_subpackages(),
            parent=parent,
            doc_string=package.get_docstring(),
            library_structure=navigation_template,
            author_name='Reuben Ferrante',
            sub_packages_link=html_directory_link,
            modules_link=html_directory_link,
            parent_directory_link=parent_directory_link,
            main_library_link=main_library_link + str(self.library),
            css_link=css_link
        )
        self._save_template_to_html(save_directory, p_name, template)

    def _get_package_html_and_parent_link(self, package, main_package_dir):
        """
        Get the relative package directory link and parent link.
        :param package:
        :param main_package_dir:
        :return:
        """
        parent = package.get_parent()
        parent_directory_link = ''

        if parent is None or parent == '':
            html_directory_link = './' + str(self.library)
        else:
            html_directory_link = './' + str(package)
            parent_directory_link = '../' + str(parent)

        return html_directory_link, parent_directory_link

    def _get_module_parent_link(self, package):
        """
        Gets the main parent html link.
        :param package:
        :return:
        """
        parent_directory_link = '../' + str(package)
        return parent_directory_link

    def _get_navigation_link(self, package, module=None):
        """
        Gets the relative link for the css files and the main home page.
        :param package:
        :param module:
        :return:
        """
        package_to_check = str(package) if module is None else str(module.get_parent())
        subpackage_index = substring_occurrences(str(package), '-')  # This package is inherently the parent.
        navigation_link, main_library_link = '', ''
        library_name = str(self.library)
        css_link = "../"

        if module is None: # We're processing a package.
            if package_to_check == library_name: # Package is the library main package
                navigation_link = './' + library_name + '/'
                main_library_link = "./"
                css_link = "../"
            elif package_to_check != library_name: # sub package
                if len(subpackage_index) == 0:
                    navigation_link = './'
                else: # Sub-package inside a package, e.g. HERCULES (main library)/some package/some sub-package/etc.
                    navigation_link = ''.join(['../' for _ in range(len(subpackage_index))])
                main_library_link = ''.join(['../' for _ in range(len(subpackage_index)+1)])
                css_link = "../" + main_library_link
        else: # .py file
            if str(package) == library_name:
                string_join = './'
                main_library_link = '../'
            else:
                string_join = '../'
                main_library_link = ''.join(['../' for _ in range(len(subpackage_index) + 2)])
            css_link = "../" + main_library_link

            navigation_link = ''.join([string_join for _ in range(len(subpackage_index)+1)]) # Modules in sub-packages

        return navigation_link, main_library_link, css_link

    def _create_library_navigation_template(self, package, module=None):
        """
        Gets the links to the package and module and creates the appropriate html file.
        :param package: package type
        :param module: default=None.
        :return: template, main_library_link, css_link
        """
        navigation_link, main_library_link, css_link = self._get_navigation_link(package, module)

        template = self.j2_env.get_template(LIBRARY_STRUCTURE).render(
            title=self.library.get_name(),
            navigation_content=[(self.library.get_subpackages(), 'Packages'),
                                (self.library.get_modules(), 'Modules')],
            directory_link=navigation_link
        )
        return template, main_library_link, css_link

    def _save_template_to_html(self, main_directory, file_name, template):
        """ Saves the created html template to disk. """
        if '.html' not in file_name[-5:]:
            file_name = ''.join([file_name, '.html'])

        if self.directory_delimiter not in main_directory[-len(self.directory_delimiter):]:
            main_directory = ''.join([main_directory, self.directory_delimiter])

        file = ''.join([main_directory, file_name])
        try:
            with open(file, "w") as f:
                f.write(template)
            return True # Success
        except Exception as e:
            logging.ERROR("Error when writing template to file in HTMLCreator. {}".format(e))
            return False # Failed

    def _create_directory(self, directory):
        """ Creates a new directory if it doesnt exist. """
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory