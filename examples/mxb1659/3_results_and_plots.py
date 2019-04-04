import time
import datetime
import shutil
import os
import sys
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import emdee


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


# We need to again load the results we want to plot.
emdeeClass = emdee.Emdee(mode='load',loc='example_output')

# For all of the plots, the save argument determines whether:
# True -- the figure will be saved with the file name/location given by 'name' arg.
# False -- the figure is just output with plt.show(). 

# The "chain" plots can look messy but tend to be the best way of visualizing whether
# or not the parameters have "burned in", where they "find" the value/range that they're
# going to continue to hover around for the remainder of the run.
# The optional hlines argument can be a dict of {"param": value} for which horizontal 
#   reference lines will be drawn on the resulting figure. This does not need to be 
#   the same length as the total number of parameters.
emdeeClass.PlotChains(save=True,name='chain.png',
                      hlines={"core_mass":1.6,"core_radius":10.4})
                      
# Typically one wishes to ignore early values where the walkers are still "wandering". 
#   Therefore you can use the burnin argument to set the number of steps to trim off the
#   beginning. For example, burnin=70 would remove the first 70 positions of each walker 
#   from the results.             
# Alternatively, the argument lastpt=True will cause only the FINAL step to be plotted.
#   This is useful for calculating percentiles and other information from the chain of 
#   results (see PrintPercentiles below), but usually makes for a pretty ugly and 
#   uninformative corner plot.
emdeeClass.PlotCorner(save=True,name='corner.png',burnin=70)

# PrintPercentiles just spits out simple "mean +upperbound -lowerbound" style values
# for a quick summary of what the "fitted" parameters are. 
# By default, the upper and lower bounds are calculated from the 84th and 16th percentile 
#   respectively (1-sigma). These can be chosen manually using the argument
#   lowmidhigh=[lower,mean,upper] (e.g. default is lowmidhigh=[16,50,84]).
# The argument lastpt=True means the percentiles are only calculated from the final step.
#   By default this is set to False, but typically early values where the walkers are
#   still "wandering" want to be ignored. Therefore one can just take values from the
#   final step, or use the burnin argument to set the number of steps to trim off the
#   beginning, just as in PlotCorner.
emdeeClass.PrintPercentiles(lastpt=True)

# PrintBestFits spits out a summary of the 'n' walkers with the best fits to the data
# (highest lnprob, or lowest chi2). Default n is 5. If save is False, just prints
# to the terminal. If save is True, saves to a file with 'name' (default: 'bestfits.txt)
emdeeClass.PrintBestFits(n=10,save=True,name='bestfits.txt')


# It should be noted that all these same plot commands could of course be used at the end
# of a "new" Emdee run to plot/save the results, all in one Python script. This example
# is only broken into chunks to illustrate functionality, and I tend to load+plot old
# results just as often or more often than running one giant single "200 walkers for 
# 600 steps, then plot when finished", just because so many things can happen along
# the way.


print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
