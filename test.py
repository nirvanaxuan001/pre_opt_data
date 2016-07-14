'''
Created on 2016-6-20

@author: Administrator
'''


import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
x= np.arange(1,10,1)
y= stats.zipf.cdf(x,2)
deep_dist = dict(zip(x,y))
print deep_dist
print x
print y
plt.plot(x,y)
plt.show()


#from scipy.stats import lognorm
#import matplotlib.pyplot as plt
#import numpy as np
#fig, ax = plt.subplots(1, 1)
#
#
#s = 0.954
#mean, var, skew, kurt = lognorm.stats(s, moments='mvsk')
#
#
#x = np.linspace(lognorm.ppf(0.01, s),
#                 lognorm.ppf(0.99, s), 100)
#ax.plot(x, lognorm.pdf(x, s),
#       'r-', lw=5, alpha=0.6, label='lognorm pdf')
#
#
#
#rv = lognorm(s)
#ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
#
#
#vals = lognorm.ppf([0.001, 0.5, 0.999], s)
#np.allclose([0.001, 0.5, 0.999], lognorm.cdf(vals, s))
#
#
#r = lognorm.rvs(s, size=1000)
#
#ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2)
#ax.legend(loc='best', frameon=False)
#plt.show()

