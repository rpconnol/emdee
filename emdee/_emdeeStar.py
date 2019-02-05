import shutil
import subprocess
import sys

class mixin:

    def _MakeInlist(self,theta):

        shutil.copy('inlist_preamble','inlist')
        f = open("inlist", "at")

        for i in range(len(theta)):
            if self.params[i] == 'Mdot':
                f.write("   epoch_Mdots(1) = {:e}\n".format(theta[i]))
            else:
                f.write("   "+self.params[i]+" = {}\n".format(theta[i]))
        
        f.write("\n/\n")

        f.close()

    
    def _RunDStar(self):
        
        # If running Python 3, need an additional kwarg to subprocess.Popen,
        # otherwise stdout is parsed as binary(?) rather than text...
        # The 'text' kwarg doesn't exist in Python 2.x though, so will error.
        #kwargs = {}
        #if sys.version_info >= (3, 0):
        #    kwargs = {'text': True}
        # EDIT: actually this might be taken care of by universal_newlines=True,
        # which is aliased by 'text' but still exists for backwards compat.

        process = subprocess.Popen(
            "./run_dStar -D "+self.dstar_dir+" -I inlist",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True)
        
        try:
            chi2 = process.stdout.readlines()[-1]
            chi2 = float(chi2.strip(' \t\n\r'))
            
            if self._debugging == True: print('dstar return = '+str(chi2))
            return chi2
        except ValueError:
            if self._debugging == True: 
                print('dstar return = BIG (couldnt capture chi2)')
            return 99999999.9
            # If the parameters are unable to construct a dStar model and
            # dStar bails out with 'NScool_evolve_model: ierr = -8' or 
            # something similar, catch the exception and return terrible chi2