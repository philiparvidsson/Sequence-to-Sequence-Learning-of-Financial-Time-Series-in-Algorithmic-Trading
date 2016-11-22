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

pymake(pdflatex.defaultConf(), {
    'name'    : 'thesis',
    'srcfile' : 'src/thesis.tex',
})
