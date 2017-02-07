#!/usr/bin/env python

#---------------------------------------
# IMPORTS
#---------------------------------------

import os
import subprocess

#---------------------------------------
# ENTRY POINT
#---------------------------------------

for fn in os.listdir(os.path.join("..", "configs")):
    if not fn.endswith(".py"):
        continue

    print "------- BEGINNING TRAINING SESSION -------"
    subprocess.call(["python", "train.py", os.path.join("..", "configs", fn)])
