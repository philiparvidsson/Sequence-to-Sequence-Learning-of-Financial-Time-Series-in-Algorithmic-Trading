#!/usr/bin/env python

#---------------------------------------
# IMPORTS
#---------------------------------------

import os
import subprocess

#---------------------------------------
# ENTRY POINT
#---------------------------------------

if not os.path.isdir(os.path.join("..", "out")):
    os.makedirs(os.path.join("..", "out"))

files = sorted([s for s in os.listdir(os.path.join("..", "configs")) if s.endswith(".py")])
i = 1
for fn in files:
    print "\n\ntraining config {} of {}...\n".format(i, len(files))
    i += 1
    with open(os.path.join("..", "out", os.path.basename(os.path.splitext(fn)[0])) + ".txt", "w") as f:
        subprocess.call(["python", "train.py", os.path.join("..", "configs", fn)], stdout=f)
