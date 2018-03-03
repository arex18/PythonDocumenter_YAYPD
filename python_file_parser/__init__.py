"""
@PACKAGEDESC: This package parses a directory, finds Python files and creates the library as a Library type found
in type_definitions. It creates a Library type ready for html processing; containing packages, modules, sub-packages etc.
The hierarchy is as follows: Library/Package/Module/Classes and Functions.
Each step has its own special documentation and tags, e.g. Class descriptions exist as docstrings
in the Class Type, but under the parent Module, which in turn sits under Package...
Current version 1.1, using Python 3.6
"""