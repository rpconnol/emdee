import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import emdee

emdeeClass = emdee.Emdee()
print(dir(emdeeClass)) # wont include some things that are defined on the fly

os.rmdir(emdeeClass.data_dir)