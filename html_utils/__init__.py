"""
@PACKAGEDESC: This package contains both HTML templates and the main python html processor.
Jinja2 is used for html. The html processor is given a library path and an output path,
and creates the necessary html files with proper links in the same directory structure as the
library. CSS files are also automatically copied to the output path, and are listed under
the "static" folder. The input must be the LibraryDefinition, as parsed from the file_parser.py
in the dir_file_utils package.
"""