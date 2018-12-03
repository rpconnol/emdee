import shutil
import subprocess

class mixin:

    def _MakeInlist(self,theta):

        shutil.copy('inlist_preamble','inlist')
        f = open("inlist", "at")

        for i in range(len(theta)):
            if self.params[i] == 'Mdot':
                f.write("   epoch_Mdots = {:e},{:d}*0.0\n".format(
                    theta[i],self.MdotIntervals))
            else:
                f.write("   "+self.params[i]+" = {}\n".format(theta[i]))
        
        f.write("\n/\n")

        f.close()

    
    def _RunDStar(self):
        
        process = subprocess.Popen(
            "./run_dStar -D "+self.dstar_dir+" -I inlist",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        chi2 = process.stdout.readlines()[-1]
        chi2 = float(chi2.strip(' \t\n\r'))

        return chi2