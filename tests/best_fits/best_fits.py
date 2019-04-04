# Tests PrintBestFits and PlotBestFits

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
if os.path.exists('load_data/README'):
    os.remove('load_data/README')


emdeeClass = emdee.Emdee(mode='load',loc='load_data')
emdeeClass.PrintParams()

emdeeClass.PrintBestFits(n=3)
emdeeClass.PrintBestFits(save=True)


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
