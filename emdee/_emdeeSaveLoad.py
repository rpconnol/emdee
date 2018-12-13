import time
import datetime
import numpy as np

import emdee

class mixin:
    
    def _LogStart(self):
        # Start a new log if one does not already exist. Log is going to contain 
        # info like date/time of creation, number of walkers, dStar parameters 
        # + bounds, etc.
        # Only use after parameters are finalized!

        print("writing new log")

        f = open(self.data_dir+"/LOG.txt", "a")

        f.write("Created: " +
            datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S') + 
            "\n")
        
        f.write("Output directory: "+self.data_dir+"\n")
        f.write("\n")

        f.write("Number of walkers: "+str(self.nwalkers)+"\n")
        
        f.write("dStar parameters:\n")
        for i in range(len(self.params)):
            p = self.params[i]
            fmt = emdee.emdeeDefaults.Format(p)
            f.write(("  "+p+"   "+fmt+" - "+fmt+"\n").format(
                self.lbounds[i],self.ubounds[i]))
        f.write("\n\n")

        f.close()


    def _LogUpdate(self):
        # Writes update to log file after GoMCMC. Contains start/end/run time 
        # info of that chunk of MCMC, and perhaps some useful info 
        # (percentiles, autocorr times, etc).
        # NOTE: Make sure _lastlogged is updated BEFORE _LogUpdate is called.

        print("updating log")

        f = open(self.data_dir+"/LOG.txt", "a")

        f.write("Update: " +
            datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S') + 
            "\n")

        f.write("Total iterations: {:d}\n".format(self._lastlogged))

        f.write(self.PrintPercentiles(print_acor=True,_log=True))
        f.write("(percentiles calculated from full chain; no burn in removal)")

        f.write("\n\n\n")
        f.close()


    def _Output(self):
        #Writes MCMC data to files after GoMCMC.

        ## STILL NONFUNCTIONAL!  May just go with one line at a time since
        ## the read/write isn't going to be that slow compared to dStar itself

        totalsteps = self._lastlogged + len(self._emceeSampler.chain[0,:,0])

        for iparam in range(len(self.params)):

            f = open(self.data_dir+"/"+self.params[iparam]+".txt", "a")

            for istep in range(
                self._lastlogged,totalsteps):

                for iwalker in range(self.nwalkers):

                    f.write("{} ".format(
                        self._emceeSampler.chain[iwalker,istep,iparam]))
                        
                f.write("\n")
            
            f.close()
        
        #self._lastlogged = totalsteps


    def _OutputOneLine(self,pos):
        #Writes single ("previous") MCMC step to files. Mostly for testing?

        for iparam in range(len(self.params)):

            f = open(self.data_dir+"/"+self.params[iparam]+".txt", "a")

            for iwalker in range(self.nwalkers):

                f.write("{} ".format(
                    pos[iwalker,iparam]))
            
            f.write("\n")
            
            f.close()
    

    def _OutputCurrentLnprob(self,lnp):
        #Writes single MCMC lnprob to file

        f = open(self.data_dir+"/last_lnprob.txt", "w")

        for iwalker in range(self.nwalkers):

            f.write("{} ".format(lnp[iwalker]))
            
        f.write("\n")
            
        f.close()


    def _UpdateLocalChain(self):

        if self._lastlogged == 0:
            self._localChain = self._emceeSampler.chain
        else:
            self._localChain = np.append(self._localChain,
                                         self._emceeSampler.chain,
                                         axis=1)
    

    # Loading stuff

    def _ReadLog(self):

        self.params = []
        self.lbounds = []
        self.ubounds = []

        flag = False

        with open(self.data_dir+'/LOG.txt') as f:

            for line in f:

                if flag == False:
                    if "dStar parameters:" in line:
                        flag = True
                
                else:
                    if line in ['\n', '\r\n']:
                        break
                    else:
                        s = line.split()
                        self.params.append(s[0])
                        self.lbounds.append(float(s[1]))
                        self.ubounds.append(float(s[3]))
                    
        print('parameters read from log')


    def _LoadLocalChain(self):

        for iparam in range(len(self.params)):

            filename = self.data_dir+"/"+self.params[iparam]+".txt"

            a = np.loadtxt(filename)

            if iparam == 0:
                (self._lastlogged,self.nwalkers) = a.shape
                self._localChain = np.zeros(
                    (self.nwalkers,self._lastlogged,len(self.params))
                    )
            
            for iwalker in range(self.nwalkers):
                for istep in range(self._lastlogged):
                    self._localChain[iwalker,istep,iparam] = a[istep,iwalker]
        
        print('chain loaded from output files')
    

    def _SetCurrentConditions(self):

        self._current_pos = self._localChain[:,-1,:]

        filename = self.data_dir+"/last_lnprob.txt"
        self._current_lnprob = np.loadtxt(filename)