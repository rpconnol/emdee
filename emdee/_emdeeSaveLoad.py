import time
import datetime

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

        print("updating log")

        f = open(self.data_dir+"/LOG.txt", "a")

        f.write("Update: " +
            datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S') + 
            "\n")

        f.write("Total iterations: {:d}\n".format(self._lastlogged))

        f.write(self.PrintPercentiles(print_acor=True,_log=True))
        f.write("(percentiles calculated from full chain; no burn in removal)")

        f.write("\n")
        f.close()


    def _Output(self):
        #Writes MCMC data to files after GoMCMC.

        print('hello world')


    def _OutputOneLine(self,pos):
        #Writes single (previous) MCMC step to files. Mostly for testing!!

        for iparam in range(len(self.params)):

            f = open(self.data_dir+"/"+self.params[iparam]+".txt", "a")

            for iwalker in range(self.nwalkers):

                f.write("{} ".format(
                    pos[iwalker,iparam]))
            
            f.write("\n")
            
            f.close()
