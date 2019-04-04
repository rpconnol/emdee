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

                if hlines is not None:
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
        

    def PrintBestFits(self,n=5,save=False,name="bestfits.txt"):
        # Grab the param values for the n walkers with the largest lnprob.
        # If save == True, save to a file (in output directory) called [name].

        # self._current_lnprob contains the current (or "loaded") lnprobs and
        # lnprob * -2.0 = chi2 from dStar (LnLike returns -chi2 / 2.0)

        ## SUMMARY ##
        # To get the best n fits, use:
        #   ind = np.argpartition(lnprob, -n)[-n:]
        # This isn't sorted in any way however, so perform the following:
        #   ind_sort = ind[np.argsort(lnprob[ind])]
        # This returns the list of indeces of the top n values of lnprob, sorted
        # LOW to HIGH. Since we actually WANT the HIGHEST lnprob ("best fit"):
        #   ind_sort = ind_sort[::-1]
        # Now ind_sort is the indeces of the n walkers that have the best fit,
        # from BEST (largest lnprob and therefore lowest chi2) to worst.
        # Step through each of these and grab all the params for that walker.

        lnprob = self._current_lnprob

        ind = np.argpartition(lnprob, -n)[-n:]  # Indeces of n largest values
        ind_sort = ind[np.argsort(lnprob[ind])] # Indeces but low to high lnprob
        ind_sort = ind_sort[::-1]               # Indeces but high to low lnprob

        # ind_sort is "the best n walkers", from best to worst chi2

        ndim = len(self.params)

        s = ""  # This will be the large string either printed or saved

        for iwalker in ind_sort:

            chi2 = lnprob[iwalker] * -2.0
            s += "chi2: "+str(chi2)+"\n"
            
            for iparam in range(ndim):
                p = self.params[iparam]
                fmt = emdee.emdeeDefaults.Format(p)
                # self._current_pos has shape [walker#,param#]
                s += ((p+" = "+fmt).format(self._current_pos[iwalker,iparam]))
                s += "\n"
                
            s += "\n"
        
        if save == True:
            f = open(self.data_dir+"/"+name, "w")
            f.write(s)
            f.close()
        else:
            print(s)
        

    #def PlotBestFits(self,name="bestfits.txt"):
        # Pull the N best fits from 'name' (default: bestfits.txt) and run+plot
        # them each individually.

        # Not yet.
