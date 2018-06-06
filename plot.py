#! /usr/bin/python3 

import pandas  as pd 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

#data selection
data=pd.read_csv("~/Desktop/wiifit/run_stab_Wed Jun  6 10:58:53 2018.csv", delimiter=',')

x=data.iloc[:,-2]
y=data.iloc[:,-1]
t=data.iloc[:,0]

# x,y,ellispe plotting
def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# Move left y-axis and bottim x-axis to centre, passing through (0,0)
ax.spines['left'].set_position(('zero'))
ax.spines['bottom'].set_position(('zero'))#
# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')#
# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# axes length
x1=np.max(x)
y1=np.max(y)
if x1 > y1:
   plt.xlim(-x1,x1)
   plt.ylim(-x1,x1)
elif x1 < y1:
   plt.xlim(-y1,y1)
   plt.ylim(-y1,y1)


nstd = 2
y=-y
cov = np.cov(x, y)
vals, vecs = eigsorted(cov)
theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
w, h = 2 * nstd * np.sqrt(vals)
ell = Ellipse(xy=(np.mean(x), np.mean(y)),
              width=w, height=h,
              angle=theta, color='black')
ell.set_facecolor('none')
ax.add_artist(ell)
plt.plot(x, y)
plt.show()




#X and Y by time

plt.subplot(2, 1, 1)
plt.plot(t,x)
plt.title('X and Y')
plt.ylabel('x position')#
plt.subplot(2, 1, 2)
plt.plot(t, y)
plt.xlabel('time (s)')
plt.ylabel('y position')#
plt.show()#



