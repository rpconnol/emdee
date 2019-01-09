import numpy as np
import matplotlib.pyplot as plt
import corner
import emdee.emdeeDefaults
import emcee

class mixin:
    
    def PlotChains(self,save=False,name="chain.png",hlines=None):

        # hlines should be a dict, i.e. hlines = {"core_mass": 1.6, ...}

        ndim = len(self.params)

        fig, axes = plt.subplots(ndim,1,sharex=True)

        for iparam in range(ndim):

            for iwalker in range(self.nwalkers):

                axes[iparam].plot(self._localChain[iwalker,:,iparam], 
                                  color='black', linewidth=0.5, alpha=0.5)

                axes[iparam].set_ylabel(self.params[iparam])

                if self.params[iparam] in hlines:
                    axes[iparam].axhline(hlines[self.params[iparam]])


        if save == True:
            plt.savefig(self.data_dir+"/"+name)
        else:
            plt.show()


    def PlotCorner(self,burnin=0,lastpt=False,save=False,name="corner.png"):

        ndim = len(self.params)

        if lastpt == True:
            samples = self._localChain[:, -1, :].reshape((-1,ndim))
        else:
            samples = self._localChain[:, burnin:, :].reshape((-1,ndim))

        fig = corner.corner(samples, labels=self.params)

        if save == True:
            plt.savefig(self.data_dir+"/"+name)
        else:
            plt.show()
    

    def PrintPercentiles(self,lowmidhigh=[16,50,84],
                         burnin=0,lastpt=False,
                         print_acor=False,_log=False):

        ndim = len(self.params)

        if lastpt == True:
            samples = self._localChain[:, -1, :].reshape((-1,ndim))
        else:
            samples = self._localChain[:, burnin:, :].reshape((-1,ndim))

        # Median, up, down
        percentiles = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), 
	                      zip(*np.percentile(samples, [16, 50, 84],axis=0)))
        percentiles = list(percentiles)
        
        s = "Percentiles:\n"
        for i in range(len(self.params)):
            p = self.params[i]
            fmt = emdee.emdeeDefaults.Format(p)
            s += (("  "+p+
                      ": "+fmt+
                      " +"+fmt+
                      " -"+fmt).format(percentiles[i][0],
                                       percentiles[i][1],
                                       percentiles[i][2]))
            if print_acor == True:
                try:
                    s += ("   (autocorrelation time = "+
                          str(self._emceeSampler.acor[i])+")")
                except emcee.autocorr.AutocorrError:
                    print("The chain is too short to calc autocorr")
            s += "\n"
        
        # if _log is True, assumes you want to write it to a file, so just
        # returns the s string. If False, just prints to stdout.
        if _log == True:
            return s
        else:
            print(s)
        
