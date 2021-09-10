# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:49:21 2020

@author: Юрий
"""
import os
import tensorflow as tf
from tensorflow import keras
from os import listdir
from os.path import isfile, join
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage 
from tensorflow.python.client import device_lib
import Fresnel_automatic as FA
import NeuralFunctions as NF

print(device_lib.list_local_devices())

        
# INPUT is considered as LABELS and OUTPUT is considered as data. 
# PURPOSE - after training give neural network data = TARGET SHAPE and receive necessary input to achive this shape. 
mypath_output='K:\\Work\\Python\\GitHub\\Fresnel\\Shapes\\Out\\'
mypath_input='K:\\Work\\Python\\GitHub\\Fresnel\\Shapes\\In\\'

# A simple search of optimal Neural Network neuron amount in a hidden layer can be performed - this is optional.
nn_output='K:\\Work\\Python\\GitHub\\Fresnel\\Output_data\\'

input_shape=1024
output_shape=1024

# The data can be compressed from initial 1024 using compression_rate. This is for testing.
compression=False
compression_rate=4

# The initial data is not separated into test and train. 
# Below the parameter that defines the separation rate. 
test_percent_separation=10 # 10 percent will be used for a test data.

# READING DATA

onlyfiles_out = [f for f in listdir(mypath_output) if isfile(join(mypath_output, f))]
items=len(onlyfiles_out)


train_arr=np.zeros(np.append(items,input_shape))
train_labels=np.zeros((items,output_shape))


onlyfiles_in = [f for f in listdir(mypath_input) if isfile(join(mypath_input, f))]
k=0
for i in onlyfiles_in:
    f=np.loadtxt(mypath_input+i)
    train_labels[k]=f
    #normalization of input
    train_labels[k]=train_labels[k]/np.sum(train_labels[k])
    k=k+1
    



k=0
for i in onlyfiles_out:
    f=open(mypath_output+i, "r")
    lines = [line for line in f.readlines()]
    f.close()
    
    #FRESNEL saved data should be pre-processed
    del lines[0:3]
    separated_line=[]
    for line in lines:
        separated_line.append(float(line.rstrip("\n").split('\t')[1]))
 
    separated_line=np.array(separated_line)
    train_arr[k]=separated_line
    k=k+1

# Filtering. Sometimes there are too high peaks that influence the normalization, they should be deleted

try: 
    for k in range (0,items):
        if np.amax(train_arr[k])/np.median(train_arr)>50:
            print('deleted')
            train_arr=np.delete(train_arr,k,0)
            train_labels=np.delete(train_labels,k,0)
            k=-1
except:
      print('bad') 

#normalization of input (labels) and output (arr=data)
  
train_labels=train_labels/np.amax(train_labels)  

max_train_for_norm=np.amax(train_arr)    
train_arr=train_arr/np.amax(train_arr)    

#train_labels = train_labels[..., np.newaxis]
#train_arr = train_arr[..., np.newaxis]
#train_labels = train_labels[..., np.newaxis]


num_test_data=int(len(train_arr[:,0])*test_percent_separation/100)

# For the moment, not random, but test is taken from the beginning. 
test_arr=np.copy(train_arr[:num_test_data,:])
test_labels=np.copy(train_labels[:num_test_data,:])

train_arr=np.copy(train_arr[num_test_data:,:])
train_labels=np.copy(train_labels[num_test_data:,:])


# Making a square shape - ideal shape.
target_shape=np.zeros(input_shape)
target_shape[400:862]=1
target_shape=ndimage.gaussian_filter(target_shape,15)
# Normalization in respect to training data
target_shape=(target_shape/np.sum(target_shape)) * np.sum(train_arr[1])


#COMPRESSION#

if compression==True:
    
    test_arr=test_arr[:,np.arange(0,1024,compression_rate)]
    test_labels=test_labels[:,np.arange(0,1024,compression_rate)]
    train_arr=train_arr[:,np.arange(0,1024,compression_rate)]
    train_labels=train_labels[:,np.arange(0,1024,compression_rate)]
    input_shape=len(np.arange(0,1024,compression_rate))

# END OF COMPRESSION

print('Data is loaded! What to do next?')
new_history=None
while True:
    choice=input('In you want to train NN with defined in code architecture, type "1". \n If you want to find optimal neuron amount for pre-defined in the code architecture, type "2". If you want to train NN additionally, type"3". If you want to exit, type "z"\n')
    if choice=='1':
        model, history = NF.train_model(input_shape, output_shape, train_arr, train_labels, nn_output)
        new_history=list(history.history['mean_squared_error'])
        NF.plotting(model, history, test_arr,test_labels, train_arr, train_labels, nn_output)
        
    elif choice=='2':
        print('Please input one by one desired neuron amount. To stop, type non-integer')
        try:
            parameter=[]
            while True:
                parameter.append(int(input()))
        except:
            print('your input:')
            print(parameter)
        while True:
            okay=input('If everything is OK, type yes to continue, or no to exit\n')
            if okay!='no' and okay!='yes':
                print("Sorry, I didn't understand that.")
                continue
            else:
                break    
        if okay=='yes':
            model, history, evaluation = NF.optimizer(input_shape, output_shape, test_arr,test_labels, train_arr, train_labels, nn_output, parameter, target_shape, max_train_for_norm)
            new_history=list(history.history['mean_squared_error'])
        elif okay=='no':
            print('Finishing work...')
            sys.exit()        
    elif choice=='3':
        if new_history==None:
            print("Can't additionaly train non-existing model")
            sys.exit()
        else: 
            model, history= NF.additional_training(input_shape, output_shape, nn_output, model, new_history, int(input('how much times?\n')), max_train_for_norm, target_shape)    
    elif choice=='z': 
        print('Finishing work...')
        sys.exit()
    else:
        print('not an option\n')
        continue
        
    




        
#evaluation=optimizer([8,16,32])

    





#evaluation=optimizer([8,16])
#additional_training(new_history, 2)
#plotting()