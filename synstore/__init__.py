__all__ = [
    "set_package_name",
    "set_cache_dir",
    "set_data_dir",
    "set_config_dir",
    "default_cache_dir",
    "default_data_dir",
    "default_config_dir",
    "list_cache",
    "list_data",
    "list_config",
    "delete_from_cache",
    "delete_from_data",
    "delete_from_config",
    "storage_factory",
]

import os
from collections.abc import Callable
from typing import TypeVar

import platformdirs
from typing_extensions import ParamSpec

_APPAUTHOR = "net_synergy"
pkg_name = ""
_CACHE_DIR = ""
_DATA_DIR = ""
_CONFIG_DIR = ""


def set_package_name(name: str) -> None:
    """Set the package name.

    This name will be used to create sub-directory at the end of the cache and
    data directories. If your platform's standard cache directory is
    `~/.cache`, synstore will use `f"~/.cache/{package_name}"` as the default
    cache for the project.
    """
    global pkg_name, _CACHE_DIR, _DATA_DIR, _CONFIG_DIR
    pkg_name = name

    _CACHE_DIR = platformdirs.user_cache_dir(pkg_name, _APPAUTHOR)
    _DATA_DIR = platformdirs.user_data_dir(pkg_name, _APPAUTHOR)
    _CONFIG_DIR = platformdirs.user_config_dir(pkg_name, _APPAUTHOR)


def _check_package_name() -> None:
    if pkg_name:
        return

    raise NameError(
        "Synstore: package name has not been set.\n\n"
        + "Use `synstore.set_package_name` to provide package name. "
        + "This should be called early in package loading (__init__.py)"
    )


def set_cache_dir(name: str) -> None:
    """Use this path in place of the platform's default cache directory.

    If you want all cached data to be saved to a different path than the
    platform's default cache (i.e. somewhere on a different storage drive), it
    can be set here.

    Note: this will still use the package name as a sub directory of the
    provided path.
    """
    global pkg_name, _CACHE_DIR

    _CACHE_DIR = os.path.join(name, pkg_name)


def set_data_dir(name: str) -> None:
    """Use this path in place of the platform's default data directory.

    If you want all data to be saved to a different path than the platform's
    default data directory (i.e. somewhere on a different storage drive), it
    can be set here.

    Note: this will still use the package name as a sub directory of the
    provided path.
    """
    global pkg_name, _DATA_DIR

    _DATA_DIR = os.path.join(name, pkg_name)


def set_config_dir(name: str) -> None:
    """Use this path in place of the platform's default config directory.

    If you want all data to be saved to a different path than the platform's
    default data directory (i.e. somewhere on a different storage drive), it
    can be set here.

    Note: this will still use the package name as a sub directory of the
    provided path.
    """
    global pkg_name, _CONFIG_DIR

    _CONFIG_DIR = os.path.join(name, pkg_name)


def default_cache_dir(path: str | None = None) -> str:
    """Find the default location to save cache files.

    If the directory does not exist it is created.

    Cache files are specifically files that can be easily reproduced,
    i.e. those that can be downloaded from the internet.

    If `path` is provided, return the cache dir with path appended to it.
    """
    _check_package_name()
    cache_dir = os.path.join(_CACHE_DIR, path) if path else _CACHE_DIR
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, mode=0o755)

    return cache_dir


def default_data_dir(path: str | None = None) -> str:
    """Find the default location to save data files.

    If the directory does not exist it is created.

    Data files are files created by a user, usually indirectly through scripts.
    It's possible they can be reproduced by rerunning the script that produced
    them but there is no guarantee they can be perfectly reproduced.

    If `path` is provided, return the data dir with path appended to it.
    """
    _check_package_name()
    data_dir = os.path.join(_DATA_DIR, path) if path else _DATA_DIR
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, mode=0o755)

    return data_dir


def default_config_dir(path: str | None = None) -> str:
    """Find the default location to save config files.

    If the directory does not exist it is created.

    Config files are files manually (or sometimes through a configuration
    routine) by the user to alter the behavior of a package.

    If `path` is provided, return the config dir with path appended to it.
    """
    _check_package_name()
    config_dir = os.path.join(_CONFIG_DIR, path) if path else _CONFIG_DIR
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, mode=0o755)

    return config_dir


def _delete_path(path: str, recursive: bool):
    if recursive and os.path.isdir(path):
        for f in os.listdir(path):
            _delete_path(os.path.join(path, f), recursive)

    if os.path.isdir(path):
        os.rmdir(path)
    else:
        os.unlink(path)


def list_cache(path: str | None = None) -> list[str]:
    """List the contents of the cache.

    If given a `path` lists the contents of the directory `path` relative to
    the default cache directory.
    """
    return os.listdir(default_cache_dir(path))


def list_data(path: str | None = None) -> list[str]:
    """List the contents of the data directory.

    If given a `path` lists the contents of the directory `path` relative to
    the default data directory.
    """
    return os.listdir(default_data_dir(path))


def list_config(path: str | None = None) -> list[str]:
    """List the contents of the config directory.

    If given a `path` lists the contents of the directory `path` relative to
    the default data directory.
    """
    return os.listdir(default_cache_dir(path))


def delete_from_cache(file: str, recursive: bool = False) -> None:
    """Delete a file or directory relative to the default cache directory.

    Parameters
    ----------
    file : str
        The location of either a file or directory relative to the default
        cache directory.
    recursive : bool, default False
        Whether to delete recursively or not. To prevent accidentally deleting
        more data than intended, to delete a non-empty directory, this must
        explicitly be set to True.

    """
    _delete_path(os.path.join(file, default_cache_dir()), recursive)


def delete_from_data(file: str, recursive: bool = False) -> None:
    """Delete a file or directory relative to the default data directory.

    Parameters
    ----------
    file : str
        The location of either a file or directory relative to the default
        data directory.
    recursive : bool, default False
        Whether to delete recursively or not. To prevent accidentally deleting
        more data than intended, to delete a non-empty directory, this must
        explicitly be set to True.

    """
    _delete_path(os.path.join(file, default_data_dir()), recursive)


def delete_from_config(file: str, recursive: bool = False) -> None:
    """Delete a file or directory relative to the default config directory.

    Parameters
    ----------
    file : str
        The location of either a file or directory relative to the default
        config directory.
    recursive : bool, default False
        Whether to delete recursively or not. To prevent accidentally deleting
        more data than intended, to delete a non-empty directory, this must
        explicitly be set to True.

    """
    _delete_path(os.path.join(file, default_config_dir()), recursive)


P = ParamSpec("P")
T = TypeVar("T")


def storage_factory(func: Callable[P, T], subdir: str) -> Callable[P, T]:
    """Wrap a storage function to work on a subdirectory.

    Generates new functions that behave like the default synstore functions but
    for a subdirectory of the projects directory.

    Examples
    --------
    > import synstore
    > from synstore import default_cache_dir, storage_factory
    > synstore.set_package_name("foo")
    > default_cache_dir()
    '/home/user/.cache/foo'
    > default_bar_cache = storage_factory(default_cache_dir, "bar")
    > default_bar_cache()
    '/home/user/.cache/foo/bar'

    """

    def wrapper(*args: P.args, **kwds: P.kwargs) -> T:
        if len(args) != 0:
            new_args = (os.path.join(subdir, args[0]),) + args[1:]  # type: ignore[call-overload]
        else:
            new_args = args

        if "path" in kwds and kwds["path"] is not None:
            kwds["path"] = os.path.join(subdir, kwds["path"])  # type: ignore[call-overload]
        else:
            kwds["path"] = subdir

        return func(*new_args, **kwds)

    return wrapper
