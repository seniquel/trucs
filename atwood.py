# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import math as mt
import scipy.integrate as spi

def atwood(x,t):
    dx=[0.]*len(x)
    dx[0]=x[2]/(m+M)
    dx[1]=x[3]/(m*(x[0]**2))
    dx[2]=(x[3]**2)/(m*(x[0]**3))-M*g+m*g*np.cos(x[1])
    dx[3]=-m*g*x[0]*np.sin(x[1])
    return dx
    
def poltocart(r):
    x=[0.]*2
    x[0]=-r[0]*np.cos(r[1])
    x[1]=-r[0]*np.sin(r[1])
    return x
    
m=1
M=10
g=10
xt=np.linspace(0,50,10000)
x0=[1.,np.pi/2,0.,0.]
x1=[1.,0.0001+np.pi/2,0.,0.]

res=spi.odeint(atwood,x0,xt)
r=res[:,0]
theta=res[:,1]
pr=res[:,2]
ptheta=res[:,3]

res1=spi.odeint(atwood,x1,xt)
r1=res1[:,0]
theta1=res1[:,1]
pr1=res1[:,2]
ptheta1=res1[:,3]

pol=[r,theta]
cart=poltocart(pol)

pol1=[r1,theta1]
cart1=poltocart(pol1)

dist=[0.]*len(xt)
for i in range(len(xt)):
    dist[i]=np.sqrt((cart[0][i] - cart1[0][i])**2 + (cart[1][i] - cart1[1][i])**2)

f = plt.figure()
ax=f.add_subplot(121)
ax.plot(cart[1],cart[0])
ax.plot(0,0,'o')
#ax=f.add_subplot(132)
#ax.plot(cart1[1],cart1[0])
#ax.plot(0,0,'o')
ax=f.add_subplot(122)
ax.plot(xt,dist)
ax.set_yscale('log')


plt.show()