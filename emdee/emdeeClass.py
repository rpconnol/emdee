# these just contain mixins for the main class, for organization
import emdee._emdeePrep
import emdee._emdeeMCMC
import emdee._emdeeStar
import emdee._emdeeSaveLoad
import emdee._emdeeResults

import datetime
import time
import os

class Emdee(emdee._emdeePrep.mixin, 
            emdee._emdeeMCMC.mixin, 
            emdee._emdeeStar.mixin, 
            emdee._emdeeSaveLoad.mixin, 
            emdee._emdeeResults.mixin):

    def __init__(self,mode='new',loc=None):

        if mode == 'load':
            print("loading previous run")

            if loc == None:
                sys.exit("Must provide a data directory to load")
            else:
                self.data_dir = loc
        
            self._ReadLog()
            self._LoadLocalChain()
            self._InitSampler()
            self._SetCurrentConditions()


        
        if mode == 'new':
            print("creating new run")

            if loc == None:
                loc = datetime.datetime.fromtimestamp(
                    time.time()).strftime('output_%Y-%m-%d_%Hh%Mm%Ss')
            self.data_dir = loc
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
                print("creating "+self.data_dir+" directory")

            self.nwalkers = 100

            self._lastlogged = 0

            self.params = []
            self.lbounds = []
            self.ubounds = []
        
        self.dstar_dir = '$DSTAR_DIR'
    
        self._debugging = False
    


    # _emdeePrep.mixin contains:
    # 

    # _emdeeRun.mixin contains:
    # 

    # _emdeeData.mixin contains:
    # 

    # _emdeeResults.mixin contains:
    # 