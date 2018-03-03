"""
@PACKAGEDESC: This library walks through an entire python library, parses each .py file, and generates html
documentation like the one you're reading now. Python "ast" and "jinja2" libraries are relied upon for parsing and
html generation respectively. Html templates are not displayed.

The library simply takes the library path and output path as inputs, no any additional intervention is needed.
Currently, only libraries written in Python 3.6 are supported, but this will be mitigated in future versions.

Current version 1.1, using Python 3.6
"""
