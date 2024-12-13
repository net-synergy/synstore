# Synstore

Consistent storage for net-synergy projects built around [platformdirs](https://pypi.org/project/platformdirs/).

Provides functions for project specific default cache and data directories and for listing and deleting files from those directories.

## Install

``` shell
pip install synstore
```

## Usage

Call `set_package_name` somewhere in the project before any `synstore` functions are needed.
The project's top `__init__.py` is likely a good place.

``` python
# foo/__init__.py

import synstore

from foo import __name__ as pkg_name

synstore.set_package_name(pkg_name)
```
