from typing import Sized


import numpy as np
import matplotlib.pyplot as plt

# height_sample1 = np.random.normal(loc=mu1, scale=sigma1, size=10000)
mu1 = 80
sigma1 = 40
height_sample1 = np.random.normal(loc=mu1, scale=sigma1, size=10000)
plt.hist(height_sample1, bins=1000, color='green')

mu2 = 60
sigma2 = 20
height_sample2 = np.random.normal(loc=mu2, scale=sigma2, size=10000)
plt.hist(height_sample2, bins=1000, color='green')
n1 = height_sample1.size
n2 = height_sample2.size
acc = []
accX = np.arange(mu2, mu1,0.01)
for xi in accX:
    nx1 = np.searchsorted(height_sample1,xi)
    nx2 = np.searchsorted(height_sample1,xi)
    acc.append((nx1+n1-nx2)/(n1+n2))
xx = np.max(acc)
print(xx,accX[acc.index(xx)])

plt.plot(accX,acc)
plt.show()