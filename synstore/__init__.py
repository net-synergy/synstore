__all__ = [
    "default_cache_dir",
    "default_data_dir",
    "list_cache",
    "delete_from_cache",
    "list_data",
    "delete_from_data",
]

import os

import platformdirs

_APPAUTHOR = "net_synergy"
pkg_name = ""


def set_package_name(name: str) -> None:
    global pkg_name
    pkg_name = name


def _check_package_name() -> None:
    if pkg_name:
        return

    raise NameError(
        "Synstore: package name has not been set.\n\n"
        + "Use `synstore.set_package_name` to provide package name. "
        + "This should be called early in package loading (__init__.py)"
    )


def default_cache_dir(path: str | None = None) -> str:
    """Find the default location to save cache files.

    If the directory does not exist it is created.

    Cache files are specifically files that can be easily reproduced,
    i.e. those that can be downloaded from the internet.

    If `path` is provided, return the cache dir with path appended to it.
    """
    _check_package_name()
    cache_dir = platformdirs.user_cache_dir(pkg_name, _APPAUTHOR)
    cache_dir = os.path.join(cache_dir, path) if path else cache_dir
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, mode=0o755)

    return cache_dir


def default_data_dir(path: str | None = None) -> str:
    """Find the default location to save data files.

    If the directory does not exist it is created.

    Data files are files created by a user. It's possible they can be
    reproduced by rerunning the script that produced them but there is
    no guarantee they can be perfectly reproduced.

    If `path` is provided, return the data dir with path appended to it.
    """
    _check_package_name()
    data_dir = platformdirs.user_data_dir(pkg_name, _APPAUTHOR)
    data_dir = os.path.join(data_dir, path) if path else data_dir
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, mode=0o755)

    return data_dir


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


def list_data(path: str | None = None) -> list[str]:
    """List the contents of the data directory.

    If given a `path` lists the contents of the directory `path` relative to
    the default data directory.
    """
    return os.listdir(default_data_dir(path))


def delete_from_data(file: str, recursive: bool = False) -> None:
    """Delete a file or directory relative to the default data directory.

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
    _delete_path(os.path.join(file, default_data_dir()), recursive)
