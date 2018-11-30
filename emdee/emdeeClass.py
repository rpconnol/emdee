# these just contain mixins for the main class, for organization
import emdee._emdeePrep
import emdee._emdeeMCMC
import emdee._emdeeStar
import emdee._emdeeSaveLoad
import emdee._emdeeResults

import datetime
import time

class Emdee(emdee._emdeePrep.mixin, 
            emdee._emdeeMCMC.mixin, 
            emdee._emdeeStar.mixin, 
            emdee._emdeeSaveLoad.mixin, 
            emdee._emdeeResults.mixin):

    def __init__(self,mode='new',loc=None):

        if mode == 'load':
            print("load stuff here")
        
        if mode == 'new':
            print("creating new run")

            if loc == None:
                loc = datetime.datetime.fromtimestamp(
                    time.time()).strftime('%Y-%m-%d_%Hh%Mm%Ss')
            self.data_dir = loc

            self.nwalkers = 100

            self._lastlogged = 0
        
        self.dstar_dir = '$DSTAR_DIR'

        self.params = []
        self.lbounds = []
        self.ubounds = []
    


    # _emdeePrep.mixin contains:
    # 

    # _emdeeRun.mixin contains:
    # 

    # _emdeeData.mixin contains:
    # 

    # _emdeeResults.mixin contains:
    # 