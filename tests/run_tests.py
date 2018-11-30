import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#import emdee
#print(emdee)

import testPrep
testPrep.run_tests()