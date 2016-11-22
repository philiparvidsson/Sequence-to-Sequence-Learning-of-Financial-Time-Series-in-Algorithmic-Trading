"""
PyMake provides automated build tasks and enormous flexibility, all without
esoteric syntax constructs!

See https://github.com/philiparvidsson/pymake for more information.
"""

#---------------------------------------
# IMPORTS
#---------------------------------------

import fnmatch
import os
import shutil
import subprocess
import sys

#---------------------------------------
# CONSTANTS
#---------------------------------------

VERSION = "0.27b"

#---------------------------------------
# GLOBALS
#---------------------------------------

# Exit code returned by the last call to the run_program() function.
_exit_code = 0

# Known targets that have been registered with the @target decorator.
_targets = {}

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def _check_target(target, dependencies=tuple()):
    """
    Checks the specified target recursively, making sure there are no circular
    dependencies.

    :param target:       Target to check for circular dependencies.
    :param dependencies: Do not specify. Used internally to track dependencies.
    """

    if target not in _targets:
        error('no such target: {}', target)
        return False

    make_func = _targets[target]
    if hasattr(make_func, '_pymake_ok'):
        return True

    if target in dependencies:
        error('circular dependency found in target: {}', target)
        return False

    for dep in get_dependencies(target):
        if not _check_target(dep, (target,) + dependencies):
            return False

    make_func._pymake_ok = True
    return True

def _def_copy_pred(srcpath, destpath):
    """
    Default file copying predicate. Does not overwrite newer files.

    :param srcpath:  Source path.
    :param destpath: Destination path.

    :return: True if the source file is newer than the destination file.
    """

    if not os.path.exists(destpath):
        return True

    # Only overwrite the file if the source is modified at a later time
    # than the destination.
    src_modified_time  = os.path.getmtime(srcpath)
    dest_modified_time = os.path.getmtime(destpath)

    return src_modified_time >= dest_modified_time

def _dict_to_obj(d):
    """
    Creates an object with properties from a dictionary.

    :param d: Dictionary to create an object with attributes form.

    :return: Object with attributes matching the dictionary keys and values.
    """

    # Simple hack to create attributes from the dictionary keys.
    o = lambda: None

    for key, value in d.iteritems():
        setattr(o, key, value)

    return o

def copy(srcpath, destpath, pattern=None, pred=_def_copy_pred):
    """
    Copies all files in the source path to the specified destination path.  The
    source path can be a file, in which case that file will be copied as long as
    it matches the specified mattern.  If the source path is a directory, all
    directories in it will be recursed and any files matching the specified
    pattern will be copied.

    :param srcpath:  Source path to copy files from.
    :param destpath: Destination path to copy files to.
    :param pattern:  Pattern to match filenames against.
    :param pred:     Predicate to decide which files to copy/overwrite.

    :return: Number of files copied.
    """

    if os.path.isfile(srcpath):
        if pattern and not fnmatch.fnmatch(srcpath, pattern):
            return 0

        if pred and pred(srcpath, destpath) == False:
            return 0

        path, filename = os.path.split(destpath)

        if not os.path.exists(path):
            # Make sure all directories needed to copy the file exist.
            create_dir(path)

        shutil.copyfile(srcpath, destpath)

        return 1

    num_files_copied = 0

    for s in os.listdir(srcpath):
        src  = os.path.join(srcpath , s)
        dest = os.path.join(destpath, s)

        num_files_copied += copy(src, dest, pattern)

    return num_files_copied

def create_dir(path):
    """
    Creates the specified directory if it does not exist.

    :param path: Path of the directory to create.
    """

    if not os.path.exists(path):
        os.makedirs(path)

def delete_dir(path):
    """
    Deletes the specified directory if it exists.  All files inside the
    directory will be deleted.

    :param path: Path of the directory to delete.

    :return: True if the path was a directory and was deleted.
    """

    if os.path.isdir(path):
        shutil.rmtree(path)
        return True

    return False

def delete_file(path):
    """
    Deletes the specified file if it exists.

    :param path: Path of the file to delete.

    :return: True if the path was a file and was deleted.
    """

    if os.path.isfile(path):
        os.remove(path)
        return True

    return False

def depends_on(*targets):
    """
    Registers dependencies for a make target.

    :params targets: Names of the dependencies.
    """

    def decorator(func):
        func._pymake_deps = targets
        return func

    return decorator

def error(s, *args):
    """
    Prints an error message.

    :param s:    Text to display.
    :param args: Text formatting arguments.
    """

    trace('error: ' + s, *args)

def find_files(path, pattern=None):
    """
    Finds all files in the specified directory that match the specified
    pattern.

    :param path:    Path to a directory to search for files in.
    :param pattern: Pattern to match filenames against.

    :return: A list containing all files in the path that matches the pattern.
    """

    sources = []

    for s in os.listdir(path):
        s = os.path.join(path, s)

        if os.path.isfile(s):
            if not pattern or fnmatch.fnmatch(s, pattern):
                sources.append(s)
        else:
            sources.extend(find_files(s, pattern))

    return sources

def make(target, conf, completed=None):
    """
    Attempts to make the specified target, making all its dependencies first.

    :param target:    Name of the target to make.
    :param conf:      Configuration settings.
    :param completed: Used to keep track of previously completed targets
                      during recursion.
    """

    if target not in _targets:
        error('no such target: {}', target)
        return

    if not completed:
        completed = []

    if target in completed:
        return

    if isinstance(conf, dict):
        conf = _dict_to_obj(conf)

    make_func = _targets[target]

    if not hasattr(make_func, '_pymake_ok') and not _check_target(target):
        return

    for dependency in get_dependencies(target):
        make(dependency, conf, completed)

    make_func(conf)
    completed.append(target)

def get_dependencies(target):
    if target not in _targets:
        error('no such target: {}', target)
        return []

    make_func = _targets[target]

    if not hasattr(make_func, '_pymake_deps'):
        return []

    return make_func._pymake_deps

def pymake(*args):
    """
    Starts the make process using the specified configuration.  When the make
    process has completed, exits the script.  The exit code will be the result
    of the last program executed by the make process.

    :param args: Make configuration.
    """

    target = sys.argv[1] if len(sys.argv) > 1 else 'all'

    d = {}
    for conf in args:
        for key, value in conf.iteritems():
            d[key] = value

    conf_obj = _dict_to_obj(d)
    make(target, conf_obj)

    sys.exit(_exit_code)

def run_program(s, args=None):
    """
    Runs the specified program with the specified arguments.

    :param s:    Name of the program to run.
    :param args: Program arguments.

    :return: Exit code returned by the executed program.
    """

    if not args:
        args = []

    global _exit_code
    _exit_code = subprocess.call([s] + args)

    return _exit_code

def target(func):
    """
    Marks a function as a make target. The function name will be its name.

    :param func: Function to register as a target.

    :return: The function passed intp the decorator.
    """

    _targets[func.__name__] = func

    return func

def trace(s=None, *args):
    """
    Displays the specified text, formatted with the specified arguments.

    :param s:    Text to display.
    :param args: Text formatting arguments.
    """

    if not s:
        print
        return

    print s.format(*args)

def warn(s, *args):
    """
    Prints a warning message.

    :param s:    Text to display.
    :param args: Text formatting arguments.
    """

    trace('warning: ' + s, *args)
