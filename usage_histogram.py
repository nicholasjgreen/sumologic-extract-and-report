# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:01:33 2017

@author: nick.green
"""
from settings import *
from sklearn import preprocessing
import time
import pickletools
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# Load the data file
X_dict = pickletools.load(data_filename)
X = np.array(list(X_dict.values()))



for feature_idx in range(X.shape[1]):
    n, bins, patches = plt.hist(X[:,feature_idx], 50, normed=1, facecolor='green', alpha=0.75)
    plt.draw()
    plt.savefig(r'plots\feature_hist_{}.png'.format(feature_idx))
    plt.show()


for idx in range(X.shape[1]):
    print('{} = {}'.format(idx, sum(X[:,idx])))


 [a for a in X[:,44] if a > 0]
 
 newX = np.array([a for a in X[:,44] if a > 0])
 n, bins, patches = plt.hist([a for a in np.exp(-newX)], 50, facecolor='green')
 
 n, bins, patches = plt.hist([a for a in np.exp(-X[:,44]) if a > 0], 50, facecolor='green')
 plt.axis([0, 500, 0, 2000])
 
 
 np.exp(-X[:,44])
 
 