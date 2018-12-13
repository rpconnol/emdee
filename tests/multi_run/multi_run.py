# Tests/demonstrates ability to call GoMCMC multiple times on the same
# emdee class. 


import time
import datetime
import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import emdee


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


emdeeClass = emdee.Emdee()

emdeeClass.AddParam("core_mass")
emdeeClass.AddParam("core_radius")
emdeeClass.PrintParams()

emdeeClass.ChangeWalkers(10)

emdeeClass.GoMCMC(3)

print(emdeeClass._localChain)
print(emdeeClass._lastlogged)

emdeeClass.GoMCMC(3)

print(emdeeClass._localChain)
print(emdeeClass._lastlogged)

emdeeClass.PlotChains(save=True,hlines={"core_mass":1.6,"core_radius":10.4})
emdeeClass.PlotCorner(lastpt=True,save=True)
emdeeClass.PrintPercentiles(lastpt=True)


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))