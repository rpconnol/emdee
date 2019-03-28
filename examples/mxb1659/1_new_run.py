import time
import datetime
import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import emdee


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


# Invoke a fresh Emdee class. 
# mode argument is 'new' by default, but shown explicitly here just for example purposes.
# loc is the subdirectory where results will be saved.
emdeeClass = emdee.Emdee(mode='new',loc='example_output')

# We'll use the core mass and radius as free parameters to "scan" over.
# Here we manually set bounds on mass (lower bound of 1.45 Msun, upper bound of 1.9 Msun).
# If no bounds are provided manually, a set of defaults appropriate to that parameter
#    is chosen (see emdee/emdeeDefaults.py for reference).
emdeeClass.AddParam("core_mass",[1.45,1.9])
emdeeClass.AddParam("core_radius")
emdeeClass.PrintParams()  # Optional, just to check, for example purposes

# Change the number of walkers, each with some initial position
emdeeClass.ChangeWalkers(100)

# "Run" the MCMC for this many steps. On each step, a new position is chosen for each
# walker based on the goodness of fit from the previous step. 
emdeeClass.GoMCMC(50)

# If there are N walkers and GoMCMC is executed  with K steps, the total number of 
# dStar "runs" will be N*K. In my experience, with 100-200 walkers, parameters are
# "burned in" around ~200 steps, though this will depend on the number of parameters
# you are scanning over and the data being fit. Try some tests on your own machine
# to determine run-time requirements (e.g. 100 walkers * 10 steps = 1000 dStar runs, 
# then use the difference between the time printed below and the time printed at the 
# beginning to estimate the wall time required for N*K total runs).


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))