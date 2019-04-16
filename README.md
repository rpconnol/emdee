Wrapper for use of the 'emcee' Python module with dStar

See docs/api.txt or the examples directory for info on how to interact with the package.

Required Python modules:
- numpy
- matplotlib
- emcee (homepage: http://dfm.io/emcee/current)
- corner (homepage: http://corner.readthedocs.io)

Development on this module began in Python 2.7 but switched to 3.x eventually.
It SHOULD work with both versions, but if you have issues related to using Python 2.7
email me or submit on Github and they should be resolvable (hopefully) with minor tweaks.



**Importing the module:**
1) Download the `emdee` repository from GitHub or checkout with SVN using the 
web URL: https://github.com/rpconnol/emdee.git. Place as preferred.
2) At the top of your project scripts, at the `emdee` directory to the path:
```
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '~/path/to/emdee')))
```
The path can be absolute or relative (see the mxb1659 example). This doesn't change your
permanent Python path, only locally within the current script.
3) Once your .py contains the above path correction, you can `import emdee` like a module.
4) Note that you want to point to the "base" `emdee` directory (the one that contains 
this readme), not the nested `emdee/emdee` directory that contains all of the source code.

**Setting up dStar first:**
1) This module should be used (either by script or terminal) from a 
**DSTAR WORKING DIRECTORY**. That means there needs to be a compiled and ready `run_dStar` 
IN the current working directory (plus anything dStar might whine about, like LOGS dir).
2) dStar must be configured to spit out a chi^2 goodness of fit, JUST the number,
as the very last line to stdout. See the "fit_lightcurve" example that comes with dStar
for ideas on how to calculate the chi^2 in `src/run.f` using clever Mdot_epochs and 
Teff_monitor, or the `src/run.f` of the mxb1659 example included here in emdee.
3) There MUST be an 'inlist_preamble' in the working directory!!!
This basically just means taking the desired inlist for the dStar run of choice,
chop off the "bottom" (the trailing slash, and any controls one might not want hanging
around), and call it 'inlist_preamble'. This file will be copied to actual 'inlist' 
before each dStar run and then the MCMC params + values will be appended, along with
the trailing slash/returns to close the file.
