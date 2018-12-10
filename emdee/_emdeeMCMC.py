import numpy as np
import emcee

class mixin:

    def GoMCMC(self, nsteps, output=True):

        if self._lastlogged == 0:
            print("Fresh run -- initializing walkers and sampler...")
            self._current_pos = self._InitWalkers()
            self._current_lnprob = None
            self._InitSampler()
            self._LogStart()

        print("Beginning MCMC iterations...")
        for i, result in enumerate(
                    self._emceeSampler.sample(self._current_pos,
                                              lnprob0=self._current_lnprob,
                                              iterations=nsteps)):
            if self._lastlogged == 0:
                print(str(i+1)+" of "+str(nsteps)+" iterations complete.")
            else:
                print(str(i+1)+" of "+str(nsteps)+" iterations complete "+
                        "("+
                        str(self._lastlogged+i+1)+
                        " of "+
                        str(self._lastlogged+nsteps)+
                        " total).")
            
            # For testing, output one line at a time
            (pos,lnprob,rstate) = result
            self._OutputOneLine(pos)  

        (self._current_pos, self._current_lnprob, rstate) = result
        self._lastlogged = i+1

        # OUTPUT!
        self._LogUpdate()
    

    def _InitWalkers(self):
        
        ndim = len(self.params)
        
        pos0 = []  # The initial positions of ALL walkers (nwalkers x ndim)

        for i in range(self.nwalkers):
            x = []
            for iparam in range(ndim):
                x.append(np.random.uniform(self.lbounds[iparam],
                                           self.ubounds[iparam]))
            pos0.append(x) # Append position of i'th walker
        
        # Return positions of all walkers. pos0 looks like (e.g.):
        # [ [mass0,radius0,Q0], [mass1,radius1,Q1], ... ]
        return pos0


    def _LnLike(self,theta):
        
        self._MakeInlist(theta)

        chi2 = self._RunDStar()

        return -chi2 / 2.0


    def _LnPrior(self,theta):

        inbounds = True

        for i in range(len(theta)):
            if (theta[i] > self.ubounds[i]) or (theta[i] < self.lbounds[i]):
                inbounds = False
        
        if inbounds == True:
            return 0.0
        else:
            return -np.inf
    

    def _LnProb(self,theta):

        lp = self._LnPrior(theta)
        if not np.isfinite(lp):
            return -np.inf
        
        ll = self._LnLike(theta)

        return lp + ll
    

    def _InitSampler(self):
        
        self._emceeSampler = emcee.EnsembleSampler(
            self.nwalkers, len(self.params), self._LnProb)
