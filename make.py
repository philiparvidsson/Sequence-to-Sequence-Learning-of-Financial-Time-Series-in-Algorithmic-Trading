#---------------------------------------
# IMPORTS
#---------------------------------------

import os, sys
sys.path.insert(0, os.path.join('build', 'pymake'))

from pymake import *

import pdflatex

#---------------------------------------
# SCRIPT
#---------------------------------------

pymake(pdflatex.default_conf(), {
    'name'    : 'thesis',
    'srcfile' : 'main.tex'
})
