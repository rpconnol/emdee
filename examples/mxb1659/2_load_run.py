import time
import datetime
import shutil
import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import emdee


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

# In this case we want to LOAD the results of a previous emdee run to pick up where
# we left off. With mode set to 'load' and loc pointing to the subdirectory containing
# a previous set of results (LOG.txt, last_lnprob.txt, etc...), an Emdee class is 
# populated with the loaded data and is ready to continue iterating. Changes to the 
# number of walkers or the parameters (and bounds) should not be made at this point.
# This is primarily for continuing runs that may have crashed, or completed successfully
# but haven't reached burn in (if running in small chunks locally, for example).
emdeeClass = emdee.Emdee(mode='load',loc='example_output')
emdeeClass.PrintParams()  # Just to check, for example

# As before, we just run another batch of iterations picking up from where the previous
# run that we loaded had left off.
emdeeClass.GoMCMC(100)


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
