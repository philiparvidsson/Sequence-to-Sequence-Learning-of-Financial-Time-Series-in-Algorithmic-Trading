"""
Template make script for pdflatex.
"""

#---------------------------------------
# IMPORTS
#---------------------------------------

import os
import time

from pymake import *

#---------------------------------------
# FUNCTIONS
#---------------------------------------

@target
@depends_on('compile')
def all(conf):
    """
    The 'all' target does not do anything on its own.  Instead, it depends on
    other targets that are needed to complete make process.

    :param conf: Make configuration.
    """

    pass

@target
def clean(conf):
    """
    Cleans the build by deleting the bin directory and all its contents.

    :param conf: Make configuration.
    """

    delete_dir(conf.bindir)

@target
def compile(conf):
    """
    This target compiles the executable program from its sources in the source
    directory.

    :param conf: Make configuration.
    """

    create_dir(conf.bindir)

    flags      = conf.flags
    job_name   = '-job-name=' + conf.name
    output_dir = '-output-directory=' + conf.bindir
    srcfile    = conf.srcfile

    run_program('pdflatex', flags + [job_name] + [output_dir] + [srcfile])

def default_conf():
    """
    Gets the default configuration.

    :return: Default configuration settings.
    """
    return {
        'bindir' : 'bin',
        'flags'  : ['-c-style-errors', '-quiet']
    }

@target
def watch(conf):
    """
    This target automatically invokes the 'compile' target after changes have
    been detected in the source file.

    :param conf: Make configuration.
    """

    last_mtime = None
    srcfile    = conf.srcfile

    while True:
        if not os.path.isfile(srcfile):
            warn('source file deleted; aborting')
            break

        mtime = os.path.getmtime(srcfile)
        if mtime <> last_mtime:
            make('compile', conf)
            last_mtime = mtime

        time.sleep(0.5)

#---------------------------------------
# SCRIPT
#---------------------------------------

if __name__ == '__main__':
    # If this script is executed directly, run pymake with the default
    # configuration.
    pymake(default_conf())
