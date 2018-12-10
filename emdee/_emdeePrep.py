'''
Mixin for main Emdee class that includes stuff for getting a run prepared
(params, walkers, dstar directory, etc)

Contains:
AddParam, ChangeBounds, PrintParams, ChangeWalkers, ChangeDStarDir
'''

import emdee.emdeeDefaults
import emdee._emdeeExceptions


class mixin:
    def AddParam(self,p,b=None):

        if self._lastlogged > 0:
            #raise emdee._emdeeExceptions.NonzeroRunCount(
            print("Cannot add parameters to a run 'in progress'")

        if p in self.params:
            print(p+" is already in the parameter list.")
        else:
            if b==None:
                [lb,ub] = emdee.emdeeDefaults.Bounds(p)
            else:
                lb = b[0]
                ub = b[1]
            
            self.params.append(p)
            self.lbounds.append(lb)
            self.ubounds.append(ub)
    

    def ChangeBounds(self,p,b):

        if self._lastlogged > 0:
            #raise emdee._emdeeExceptions.NonzeroRunCount(
            print("Cannot change bounds of a run 'in progress'")

        lb = b[0]
        ub = b[1]

        if p in self.params:
            idx = self.params.index(p)

            self.lbounds[idx] = lb
            self.ubounds[idx] = ub
        else:
            print(p+" is not in the current parameter list.")
    

    def PrintParams(self,printbounds=True):

        if printbounds is True:
            for i in range(len(self.params)):
                fmt = emdee.emdeeDefaults.Format(self.params[i])
                print((self.params[i]+": "+fmt+" - "+fmt).format(
                    self.lbounds[i],self.ubounds[i]))
        else:
            for p in self.params:
                print(p)
    

    def ChangeWalkers(self,n):

        if self._lastlogged > 0:
            #raise emdee._emdeeExceptions.NonzeroRunCount(
            print("Cannot change walkers for a run 'in progress'")

        if (n%2 == 0) and (n >= 2*len(self.params)):
            print("Setting number of walkers: "+str(n))
            self.nwalkers = n
        else:
            print("NOTE: Number of walkers must be even and more than")
            print("twice the number of parameters (or emcee gets upset).")
    

    def ChangeDStarDir(self,newdir):

        self.dstar_dir = newdir