# The main class
from emdee.emdeeClass import Emdee

# These just contain mixins for the main class, for organization
import emdee._emdeePrep
import emdee._emdeeMCMC
import emdee._emdeeStar
import emdee._emdeeSaveLoad
import emdee._emdeeResults

import emdee.emdeeDefaults
import emdee._emdeeExceptions

import numpy as np
import matplotlib.pyplot as plt
import datetime
import time


# Should just be able to import emdee, and then create a class with:
# my_emdee_class = emdee.Emdee(args)
# All mixins and everything happens under the hood.