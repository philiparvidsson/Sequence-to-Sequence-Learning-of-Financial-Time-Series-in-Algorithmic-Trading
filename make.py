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
    name = os.path.join(conf.bindir, conf.name)
    run_program('bibtex', [ '--include-directory', conf.srcdir, name ])

pymake2({
    'name'    : 'thesis',
    'srcfile' : 'main.tex'
})
