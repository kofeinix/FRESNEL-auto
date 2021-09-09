# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 20:31:49 2021

@author: Юрий
"""
import numpy as np
from scipy import interpolate, ndimage
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from math import exp

# The lenght of the generated file is supposed to be 1024
# To make sure that the distribution doesn't touch the borders (which is bad for optical calculations), introduce xfinish
# Start point is not limited

xfinish=862

def random_poly_fit(x):
    l=0
    h=1
    degree = np.random.randint(2,10)
    c_points = np.random.randint(10,25)
    cx = np.linspace(0,1,c_points)
    cy = np.random.rand(c_points)
    cy[0]=cy[1]=cy[-1]=cy[-2]=0
    z = np.polyfit(cx, cy, degree)
    f = np.poly1d(z)
    sub_x_len=np.random.randint(300,xfinish)
    sub_x=np.linspace(0,1,sub_x_len)
    y = f(sub_x)
    # l,h=np.sort(np.random.rand(2))
    y = MinMaxScaler(feature_range=(l,h)).fit_transform(y.reshape(-1, 1)).reshape(-1)
    y_new=np.zeros_like(x)
    y_new[xfinish-len(y):xfinish]=y
    return y_new

# Cubic Spline Interpolation
def random_cubic_spline(x):
    l=0
    h=1
    c_points = np.random.randint(5,15)
    cx = np.linspace(0,1,c_points)
    cy = np.random.rand(c_points)
    cy[0]=cy[1]=cy[-1]=cy[-2]=0
    z = interpolate.CubicSpline(cx, cy)
    sub_x_len=np.random.randint(300,xfinish)
    sub_x=np.linspace(0,1,sub_x_len)
    y = z(sub_x)
    # l,h=np.sort(np.random.rand(2))
    y = MinMaxScaler(feature_range=(l,h)).fit_transform(y.reshape(-1, 1)).reshape(-1)
    y_new=np.zeros_like(x)
    y_new[xfinish-len(y):xfinish]=y
    return y_new

# Exponential function
def random_exponential(x):
    Expon=np.zeros_like(x)
    cy = xfinish#np.random.randint(0,len(x))
    #if cy<200:
    #    cy=cy+200
    coeff=np.random.randint(50,250)/10000
    for i in range(0, cy, 1):
        Expon[i]=exp(-abs(cy-i)*coeff)
    return Expon


def random_trap(x):
    
    sub_x_len=np.random.randint(300,xfinish)
    sub_x=np.linspace(0,1,sub_x_len)
    out=np.zeros_like(sub_x)
    cy = np.random.rand(2)    
    out[0]=cy[0]
    out[-1]=cy[1]
    a_coeff=(cy[1]-cy[0])/(sub_x[-1]-sub_x[0])
    b_coeff=cy[0]
    for i in range(1,len(out)-1):
        out[i]=a_coeff*sub_x[i]+b_coeff
    out_real=(np.zeros_like(x))
    out_real[xfinish-sub_x_len:xfinish]=out
    return out_real

# Looks similar to the Bragg curve (energy loss curve of particles in a material)
def rand_bragg_like(x):
    x=np.arange(len(x))
    xstart=np.random.randint(0,len(x)/2)
    degree=np.random.uniform(low=1.0, high=10.0)
    coeff=np.random.uniform(low=1.0, high=10.0)
    curve= coeff*((x-xstart)/len(x)) ** degree
    curve[:xstart]=0    
    Expon=np.zeros((len(x),))
    exp_step=np.random.randint(10,100)
    for i in range(0,xfinish,1):
        Expon[i]=exp(i/xfinish*exp_step)
    Expon=Expon/np.amax(Expon)   
    Expon=-1*Expon+1
    Expon[xfinish]=0
    curve=curve*Expon
    curve[xfinish:]=0
    curve=curve/np.amax(curve)
    return(curve)    

# func is a random choice among all the random functions. 
# But you may chooce any specific function

def rand_func_generator():
    func_families = [random_poly_fit, random_cubic_spline, random_exponential, random_trap, rand_bragg_like]
    func = np.random.choice(func_families)
    x = np.linspace(0,1,1024)
    y = func(x)
    #new_size=len(y)
    #nokorimono=int(1024-new_size)
    #start_point=np.random.randint(100,nokorimono-100)
    #xx=np.linspace(0,1,1024)
    #yy=np.zeros((1024,))
    #yy[start_point:start_point+new_size]=y
    #yy=ndimage.gaussian_filter(yy, np.random.choice([0.1,20]))
    y=ndimage.gaussian_filter(y,np.random.uniform(low=0.5, high=20.0))    
    plt.plot(y)
    plt.show()
    return(y)
