# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:57:09 2015

@author: Edgar
"""

def plotSomething():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from pylab import figure, savefig
    import numpy as np
    import gc      
    
    a = np.arange(1000000)
    b = np.random.randn(1000000)
    
    fig = plt.figure(num=1, dpi=100, facecolor='w', edgecolor='w')
    fig.set_size_inches(10,7)
    ax = fig.add_subplot(111)
    ax.plot(a, b)
    
    fig.clf()
    plt.close()
    del a, b
    gc.collect()
    

resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
for ii in range(1000):
    if ii%10 ==0:
        print('plotting %s... \t' %ii)
    plotSomething()