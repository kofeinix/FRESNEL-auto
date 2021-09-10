# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:17:32 2021

@author: Юрий
"""
import os
import tensorflow as tf
from tensorflow import keras
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage 
from tensorflow.python.client import device_lib
import Fresnel_automatic as FA

def train_model(input_shape, output_shape, train_arr,train_labels, nn_output):
    model = keras.Sequential([
        keras.layers.Dense(input_shape, input_shape=(input_shape,)),
        keras.layers.Dense(16),
        keras.layers.Softmax(),
        keras.layers.Dense(16),
        keras.layers.Softmax(),
        keras.layers.Dense(output_shape)
    ])
    
    model.compile(optimizer='adam', 
                  loss='mse',
                  metrics=['mean_squared_error'])
    
    model.summary()
    
    # Here the parameters can be changed at will
    with tf.device('/device:GPU:0'):
        history=model.fit(train_arr,train_labels, batch_size=32, epochs=1000,verbose=1, validation_split=0.1)
    
    try:
        os.mkdir(nn_output+'model\\')
    except:
        pass
    model.save(nn_output+'model\\trained_model')
    return(model, history)


## This fuction created neural networks with different neuron amount, specified in "parameter".
## It trains the NN and evaluates it for each value in parameter.
## It saves the predicted result, which is a label, which is input pulse shape.
## Then in generates the output using the FRESNEL and compares in with the square shape.
## 
def optimizer(input_shape, output_shape, test_arr,test_labels, train_arr, train_labels, nn_output, parameter, target_shape, max_train_for_norm):
    #evaluation has both standard (0 column) and modified (1st column) deviation values
    evaluation=np.zeros((2,len(parameter)))
    try:
        os.mkdir(nn_output+'optimizer\\')
    except:
        pass
    try:
        os.mkdir(nn_output+'optimizer\\In\\') 
        os.mkdir(nn_output+'optimizer\\Out\\') 
    except:
        pass    
 
    k=0    
    for i in parameter:
        model = keras.Sequential([
        keras.layers.Dense(input_shape, input_shape=(input_shape,)),
        keras.layers.Dense(i),
        keras.layers.Softmax(),        
        keras.layers.Dense(i),
        keras.layers.Softmax(),

        keras.layers.Dense(output_shape)
        ])

        model.compile(optimizer='adam', 
                      loss='mse',
                      metrics=['mean_squared_error'])
        
        #parameters can be modified
        with tf.device('/device:GPU:0'):
            history=model.fit(train_arr,train_labels, batch_size=32, epochs=1000, verbose=1, validation_split=0.1)
        
        evaluation[0,k] = model.evaluate(test_arr, test_labels, verbose=1)[0]
        predicted_out=model.predict(target_shape[np.newaxis,...,])[0,:]
        predicted_out_filtered=ndimage.gaussian_filter(predicted_out, 15)
        predicted_out_filtered[:350]=0
        np.savetxt(nn_output+'optimizer\\In\\'+str(k)+'.txt', predicted_out_filtered)
        
        # generating the output that should ideally be square
        FA.generate_one(input_name=str(k), pusle_shape_folder=nn_output+'optimizer\\')
        predicted_result=open(nn_output+'optimizer\\Out\\Out'+str(k)+'.txt', "r")
        predicted_lines = [line for line in predicted_result.readlines()]
        predicted_result.close()
        separated_line=[]
        del predicted_lines[0:3]
        for line in predicted_lines:
            separated_line.append(float(line.rstrip("\n").split('\t')[1]))
        predicted_result_array=np.array(separated_line)/max_train_for_norm
        
        #the difference of model results and the ideal shape 
        evaluation[1,k]= model.evaluate(np.swapaxes(predicted_result_array[..., np.newaxis],0,1), np.swapaxes(target_shape[..., np.newaxis],0,1), verbose=1)[0]
        plt.plot(target_shape, label='target')        
        plt.plot(predicted_result_array, label='output')
        plt.title(str(i)+'neurons in the hidden layer')
        plt.legend()
        plt.savefig(nn_output+'optimizer\\testing_neurons='+str(i)+'.jpg', dpi=500,bbox_inches='tight')
        plt.close()
        k+=1
    return(model, history, evaluation)


# This can be used to additionaly train Neural Network
# The defined by NN value is loaded into FRESNEL, then FRESNEL output and input are once again used to train NN

def additional_training(input_shape, output_shape, nn_output, model, new_history, train_times, max_train_for_norm, target_shape):
    name_i=1
    for i in range(0,train_times):   
        try:
            os.mkdir(nn_output+'additional\\')
        except:
            pass
        try:
            os.mkdir(nn_output+'additional\\In\\') 
            os.mkdir(nn_output+'additional\\Out\\')      
        except:
            pass

        k=0    
        #target_shape=np.zeros(1024)
        #target_shape[400:862]=1
        #target_shape=ndimage.gaussian_filter(target_shape,40)
        #target_shape=(target_shape/np.sum(target_shape)) * np.sum(train_arr[1])
        predicted_out=model.predict(target_shape[np.newaxis,...,])[0,:]
        predicted_out_filtered=ndimage.gaussian_filter(predicted_out, 15)
        predicted_out_filtered[:300]=0
        np.savetxt(nn_output+'additional\\In\\'+'additional_pass='+str(name_i)+'.txt', predicted_out_filtered)
        plt.plot(predicted_out_filtered)
        plt.title('input_at_pass'+str(name_i))
        plt.savefig(nn_output+'additional\\'+'input_additional_training_pass='+str(name_i), dpi=500,bbox_inches='tight')
        plt.show()
        plt.close()
    
        FA.generate_one(input_name='additional_pass='+str(name_i), pusle_shape_folder=nn_output+'additional\\')
        predicted_result=open(nn_output+'additional\\Out\\Out'+'additional_pass='+str(name_i)+'.txt', "r")
        predicted_lines = [line for line in predicted_result.readlines()]
        predicted_result.close()
        del predicted_lines[0:3]
        separated_line=[]
        for line in predicted_lines:
            separated_line.append(float(line.rstrip("\n").split('\t')[1]))
        predicted_result_array=np.array(separated_line)/max_train_for_norm
        plt.plot(predicted_result_array)
        plt.title('output_at_pass'+str(name_i))
        plt.savefig(nn_output+'additional\\'+'out_'+str(name_i), dpi=500,bbox_inches='tight')
        plt.close()
        ## Additional fitting
        history=model.fit(predicted_result_array[np.newaxis,...,],predicted_out_filtered[np.newaxis,...,], epochs=2,verbose=1)
        new_history=new_history+list(history.history['mean_squared_error'])
        name_i=name_i+1
    return(model, new_history)

def plotting(model,history, test_arr,test_labels, train_arr, train_labels, nn_output):
    
    try:
        os.mkdir(nn_output+'Images\\')
    except:
        pass
    test_loss, test_acc = model.evaluate(test_arr, test_labels, verbose=1)
   
    #####################TEST#####################

    opmax=5 if (len(test_labels)>5) else len(test_labels)
    if opmax==1:
        raise Exception('Need more data')
    fig, axs = plt.subplots(opmax, figsize=(5,10))
    for op in range(opmax):
        axs[op].plot(test_arr[op],'-', color='grey', label='test')
        axs[op].plot(model.predict(test_arr[op][np.newaxis,...,])[0,:], label='predicted')
        axs[op].plot(test_labels[op], label='expected')
    axs[0].legend()
    plt.savefig(nn_output+'Images\\'+'comparation of test.png',dpi=200)
    plt.close()

    
    #####################TRAIN#####################
    opmax=5 if len(train_labels)>5 else len(train_labels)
    if opmax==1:
        raise Exception('Need more data')   
    fig, axs = plt.subplots(opmax, figsize=(opmax,2*opmax))
    for op in range(opmax):
        axs[op].plot(train_arr[op],'-', color='grey', label='output shape')
        axs[op].plot(model.predict(train_arr[op][np.newaxis,...,])[0,:], label='predicted input')
        axs[op].plot(train_labels[op], label='expected input')
    axs[0].legend()
    plt.savefig(nn_output+'Images\\'+'comparation_of_desired_and_achieved_plots.png',dpi=200)
    plt.close()

    # summarize history for loss

    plt.plot(np.arange(100,1000), history.history['mean_squared_error'][100:1000], color='blue')
    plt.plot(np.arange(100,1000), history.history['val_mean_squared_error'][100:1000], color='red')
    plt.title('model accuracy')
    plt.ylabel('mean_squared_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(nn_output+'Images\\'+'MeanAbsolutePercentageError_from_100s_epoch.png',dpi=200)
    plt.close()

    # summarize history for loss
    plt.plot(history.history['loss'], color='blue')
    plt.plot(history.history['val_loss'], color='red')
    plt.title('model loss')
    plt.ylabel('MSE')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(nn_output+'Images\\'+'MeanAbsolutePercentageError.png',dpi=200)
    plt.close()

    target_shape=np.zeros(1024)
    target_shape[400:862]=1
    target_shape=ndimage.gaussian_filter(target_shape, 10)
    target_shape=(target_shape/np.sum(target_shape)) * np.sum(train_arr[1])
    target_shape=target_shape[np.arange(0,1024,1)]
    
    predicted_out=model.predict(target_shape[np.newaxis,...,])[0,:]
    
    predicted_out_filtered=ndimage.gaussian_filter(predicted_out, 10)
    
    plt.plot(predicted_out_filtered)
    np.savetxt(nn_output+'Images\\'+'input_for_square_output.txt', predicted_out_filtered)
