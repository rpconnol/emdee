# Tests load capabilities

import time
import datetime
import shutil
import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import emdee


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


if os.path.exists('load_data'):
    shutil.rmtree('load_data')
shutil.copytree('test_data','load_data')
os.remove('load_data/README')


emdeeClass = emdee.Emdee(mode='load',loc='load_data')
emdeeClass.PrintParams()
#print(emdeeClass.nwalkers)
#print(emdeeClass._lastlogged)
#print(emdeeClass._current_pos)
#print(emdeeClass._current_lnprob)

emdeeClass.PlotChains(name='chain_before.png',save=True,
                      hlines={"core_mass":1.6,"core_radius":10.4})
emdeeClass.PlotCorner(name='corner_before.png',lastpt=True,save=True)
emdeeClass.PrintPercentiles(lastpt=True)


emdeeClass.GoMCMC(3)
#print(emdeeClass._lastlogged)

emdeeClass.PlotChains(name='chain_after.png',save=True,
                      hlines={"core_mass":1.6,"core_radius":10.4})
emdeeClass.PlotCorner(name='corner_after.png',lastpt=True,save=True)
emdeeClass.PrintPercentiles(lastpt=True)


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))