import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import emdee


testEmdee = emdee.Emdee(mode='new')
print()

testEmdee.AddParam('core_mass')
testEmdee.AddParam('core_radius',gaussian_init=[10.4,0.1])
testEmdee.AddParam('Qimp',gaussian_init=[20.0,100.0])
testEmdee.ChangeWalkers(10)
print()

pos0 = testEmdee._InitWalkers()
print(pos0)
print('The first column should be uniform masses between 1.4 and 2.0')
print('The second coulmn should be radii in a narrow Gaussian around 10.4')
print('The third column should be Qimp in a VERY wide Gaussian around 20, with some exact 20s mixed in (testing bounds)')
