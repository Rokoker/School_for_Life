import scipy
import numpy as np
#E=0.04
#N0=0.002
#porog = 1

##E=0.012
##N0=0.02
##porog = 1
##
##Flt = scipy.stats.norm.cdf((np.log(porog)-E/N0)/(2*E/N0)**(1/2))
##D = scipy.stats.norm.cdf((np.log(porog)+E/N0)/(2*E/N0)**(1/2))
##print("trevoga = ", Flt)
##print("obn = ", D)
##print("porog = ", np.log(porog)+E/N0)
Fl = 10**-9
print(scipy.stats.norm.cdf(0))

