# Yet Another Python Documenter - YAYPD

There's Sphinx, and it's hard to beat. But I didn't like the generation process;
having to go through a set of steps and further documentation just to get the documentation
you actually want. [Luckily, there are open source services that host the generated documentation
online.](https://readthedocs.org/)

I wanted a simple program that accepts an input path, output path, and it does the rest in 2 seconds.
This is the result of that effort. Developed in Python 3.6.

## Usage

The program accepts 3 inputs:

* Input path
* Output path
* File directory delimiter (Optional, default : '-')

Run from command line:

```
python pydoc.py -h

usage: pydoc.py [-h] [-i LIBRARY_PATH] [-o OUTPUT_PATH] [-c SPLIT_CHAR]

YAYPD! Yet Another Python Documenter

optional arguments:
  -h, --help            show this help message and exit
  -i LIBRARY_PATH, --library_path LIBRARY_PATH
                        Python project/package/module path, e.g. C:/MyProject
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path where to output the docs. Folder doesn't need to
                        exist.
  -c SPLIT_CHAR, --split_char SPLIT_CHAR
                        Separation character to add to the output folder's
                        name torepresent a directory structure, e.g.
                        MyProject/blog/main.py --> blog-main.html

```
Example:
```
python pydoc.py -i C:/MyProject -o C:/username/Desktop/Documentation
```

For a project structured as:

```
C:/MyProject

MyProject
|-- __init__.py
|   script.py
|-- Package1
|   +-- __init__.py
|   +-- module1script.py
|-- Package2
|   +-- __init__.py
|   +-- module2script.py
```
The output would be:
```
C:/username/Desktop/Documentation/MyProject (directory created or overwritten)

MyProject
|-- __init__.py.html
|   script.py.html
|   Package1.html (these contain the descriptions, imports, etc. of each sub-package)
|   Package2.html
|-- Package1
|   +-- __init__.py.html
|   +-- module1script.py.html
|-- Package2
|   +-- __init__.py.html
|   +-- module2script.py.html
MyProject.html (entry point or "index.html")
```

Note that if there are any errors in your python scripts, the documenter will skip that file due
to the usage of [*ast*](https://docs.python.org/3/library/ast.html) library.

Makes use of jinja2 for html.

## Output

The initial page shows the project description, modules, sub-packages and imports. This
holds for all packages. All files are accessible via relative-links, so each file can be clicked and viewed.
Classes, functions and their corresponding variables are displayed sequentially.

File types which are not .py will still work, but css styling might not. This is  a TODO.

The parser picks up any native function/class/package/variable documentation as well as imports as defined in PEP8. Custom tags can also be specified and picked up: 
```
PACKAGE_DESCRIPTOR = '@PACKAGEDESC'
FILE_DESCRIPTOR = '@FILEDESC'
CLASS_DESCRIPTOR = '@CLASSDESC'
FUNC_DESCRIPTOR = '@FUNCDESC'
AUTHOR_DESCRIPTOR = '@AUTHOR'
DATE_DESCRIPTOR = '@DATE'
```

Note that all css files are automatically copied to the output directory.
## TODOs (Maybe)

1. Fix styling; styling should be present for all files irrispective of extension.
2. Add TODO parser and display TODOs or any other user defined tags for every file.
3. Make user defined tags accessible from the command line, such as those found in python_file_parser/filetags.py
4. Add support for other Python PEP styles.
5. Add logs.
6. Search.

## Version and Author

v1.0.1, tested on Windows 64-bit.

Reuben Ferrante 