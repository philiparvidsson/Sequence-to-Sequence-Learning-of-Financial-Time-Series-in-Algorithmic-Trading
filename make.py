#!/usr/bin/env python
import os, sys
sys.path.insert(0, os.path.join('build', 'pymake2'))

from pymake2 import *

from pymake2.template.latex import pdflatex
from pymake2.template.util  import fswatcher

@default_target(depends=[ 'compile' ])
def all(conf):
    pass

@after_target('compile')
def bibtex(conf):
    bindir = os.path.abspath(conf.bindir)

    cwd = os.getcwd()
    os.chdir(conf.srcdir)

    bindir = os.path.relpath(bindir, os.getcwd())
    name = os.path.join(bindir, conf.name)

    run_program('bibtex', [ name ])

    os.chdir(cwd)

    # Set the modified time and rerun pdflatex to insert citations properly.

    srcfile = os.path.join(conf.srcdir, conf.srcfile)

    os.utime(srcfile, None)
    pdflatex.compile(conf)

    os.utime(srcfile, None)
    pdflatex.compile(conf)

pymake2({
    'name'    : 'thesis',
    'srcfile' : 'main.tex'
})
