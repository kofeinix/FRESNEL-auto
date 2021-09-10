# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 02:51:04 2021

@author: Юрий
"""

import pyautogui, pyperclip, keyboard
pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True
#in order to immidiately stop the program, move mouse to one of the corners of the screen
import os
import sys
import PIL 
from skimage import io
import numpy as np 
import RandFuncGen as RFG
import time
import glob
import cv2
def paste(text: str):    
    buffer = pyperclip.paste()
    pyperclip.copy(text)
    keyboard.press_and_release('ctrl + v')
    time.sleep(0.1)    
    pyperclip.copy(buffer)

#time for a single calculation should be modified according to the scheme difficulty and PC performance
wait_time=15

#define how many files should be generated
how_much_files=10

#All data will be labeled with a number starting from start_i.
#If rinning the code several times, this should be changed not to over-write data.
start_i=1010

#If you wish to clean all the data in the folder, for example if you found a mistake in the scheme, make this True
clean_start=False

#If you already have an input and want to receive an output, put the input name here.
input_name='S1000'

#all path should be set according to the data and Fresnel.exe location
path_to_screenshots='K:\\Work\\Python\\GitHub\\Fresnel\\Screenshots\\'
path_to_fresnel='K:\\Work\\Fresnel\\fresnel.exe'

#Fresnel requires the project file in .scm and some pulse shape in .pls format. 
project_name='K:\Work\Fresnel\Fresnel_examples\Elf_95_compare_24.scm'
pulse_name='K:\Work\Fresnel\Fresnel_examples\Pulse_initial.pls'

#the random input and corresponding output files folder location
pusle_shape_folder='K:\\Work\\Python\\GitHub\\Fresnel\\Shapes\\'



def generator_many_files(start_i, samples_num, pusle_shape_folder=pusle_shape_folder):
    i=start_i
    os.startfile(path_to_fresnel)
    time.sleep(3)    
    
    #The first cycle is to define the buttons positions. If do it every time, the mistake possibility increases.
    #The confidence levels can be adjusted in order of unsatisfactory quality. 
    #This can happen if the screen resolution differs from the one used for testing (2K)
    
    file_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'File.JPG', confidence=0.6)
    pyautogui.click(file_button_pos)
    
    open_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Open.JPG', confidence=0.8)
    pyautogui.moveTo(open_button_pos)
    pyautogui.click()
    paste(project_name)
    pyautogui.press('enter')  
    
    source_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Source.JPG', confidence=0.9)
    pyautogui.click(source_button_pos, clicks=2)
    
    
    load_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Load_from_file.JPG', confidence=0.6)
    pyautogui.click(load_button_pos)
    
    open_pulse_button_pos=pyautogui.locateOnScreen(path_to_screenshots+'Open_pulse.JPG', confidence=0.8)
    pyautogui.click(open_pulse_button_pos)
    paste(pulse_name)
    time.sleep(1) 
    pyautogui.press('enter')  
    
    
    time_button_pos=pyautogui.locateOnScreen(path_to_screenshots+'Time.JPG', confidence=0.6)
    pyautogui.click(time_button_pos)
    
    pulse_shape_choose_button=pyautogui.locateOnScreen(path_to_screenshots+'Pulse_shape_choose.JPG', confidence=0.6)
    pyautogui.click(pulse_shape_choose_button)
    
    #Using the RandFuncGen.py 
    
    time_shape=RFG.rand_func_generator()
    np.savetxt(pusle_shape_folder+'In\\S'+str(i)+'.txt', time_shape)
    
    browse_shape_button=pyautogui.locateOnScreen(path_to_screenshots+'Browse.JPG', confidence=0.9)
    pyautogui.click(browse_shape_button)
    
    open_shape_button=pyautogui.locateOnScreen(path_to_screenshots+'Open_pulse.JPG', confidence=0.8)
    pyautogui.click(open_shape_button)
    paste(pusle_shape_folder+'In\\S'+str(i)+'.txt')
    time.sleep(1) 
    pyautogui.press('enter')  
    
    ok_shape_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Ok.JPG', confidence=0.6)
    pyautogui.click(ok_shape_button_pos)
    
    time_plot_button_pos_1=pyautogui.locateCenterOnScreen(path_to_screenshots+'Time_plot.JPG', confidence=0.9)
    pyautogui.click(time_plot_button_pos_1)
    
    launch_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Launch.JPG', confidence=0.6)
    pyautogui.click(launch_button_pos)
    
    time.sleep(wait_time) 
        
    time_plot_button_pos_2=pyautogui.locateCenterOnScreen(path_to_screenshots+'Time_plot.JPG', confidence=0.9)
    pyautogui.click(time_plot_button_pos_2)
    
    save_plot_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Save.JPG', confidence=0.9)
    pyautogui.click(save_plot_button_pos)
    
    save_plot_button_path_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'File_name_select.JPG', confidence=0.8)
    pyautogui.click(save_plot_button_path_pos)
    
    paste(pusle_shape_folder+'Out\\'+'Out'+str(i)+'.txt')
    
    time.sleep(1) 
    pyautogui.press('enter')  
    
    #Fresnel, unfortunatelly, has problems when changing pulse or scheme parameters and should be reloaded every time
    os.system("TASKKILL /F /IM fresnel.exe")
    time.sleep(3)    
        
    
    for i in range(start_i+1,start_i+1+samples_num):
        print(i,'/',samples_num)
        
        os.startfile(path_to_fresnel)
        time.sleep(3)    
        
        pyautogui.click(file_button_pos)
        
        pyautogui.moveTo(open_button_pos)
        pyautogui.click()
        paste(project_name)
        pyautogui.press('enter')  
        
        pyautogui.click(source_button_pos, clicks=2)
        
        
        pyautogui.click(load_button_pos)
        
        pyautogui.click(open_pulse_button_pos)
        paste(pulse_name)
        time.sleep(1) 
        pyautogui.press('enter')  
    
        
        pyautogui.click(time_button_pos)
        
        pyautogui.click(pulse_shape_choose_button)
        
        #Using the RandFuncGen.py 

        time_shape=RFG.rand_func_generator()
        np.savetxt(pusle_shape_folder+'In\\S'+str(i)+'.txt', time_shape)
        
        pyautogui.click(browse_shape_button)
        
        pyautogui.click(open_shape_button)
        paste(pusle_shape_folder+'In\\S'+str(i)+'.txt')
        time.sleep(1) 
        pyautogui.press('enter')  
        
        pyautogui.click(ok_shape_button_pos)
    
        pyautogui.click(time_plot_button_pos_1)
    
        pyautogui.click(launch_button_pos)
        
        time.sleep(wait_time) 
            
        pyautogui.click(time_plot_button_pos_2)
    
        pyautogui.click(save_plot_button_pos)
    
        pyautogui.click(save_plot_button_path_pos)
        
        paste(pusle_shape_folder+'Out\\'+'Out'+str(i)+'.txt')
        
        time.sleep(1) 
        pyautogui.press('enter')  
        
        os.system("TASKKILL /F /IM fresnel.exe")
        time.sleep(3)    
    return()

#If you want to generate output upon already present input

def generate_one(input_name, pusle_shape_folder=pusle_shape_folder):

    os.startfile(path_to_fresnel)
    time.sleep(3)    
    
    file_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'File.JPG', confidence=0.6)
    pyautogui.click(file_button_pos)
    
    open_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Open.JPG', confidence=0.8)
    pyautogui.moveTo(open_button_pos)
    pyautogui.click()
    paste(project_name)
    pyautogui.press('enter')  
    
    source_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Source.JPG', confidence=0.9)
    pyautogui.click(source_button_pos, clicks=2)
    
    
    load_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Load_from_file.JPG', confidence=0.9)
    pyautogui.click(load_button_pos)
    
    open_pulse_button_pos=pyautogui.locateOnScreen(path_to_screenshots+'Open_pulse.JPG', confidence=0.8)
    pyautogui.click(open_pulse_button_pos)
    time.sleep(1) 
    paste(pulse_name)
    time.sleep(1) 
    pyautogui.press('enter')  
    
    
    time_button_pos=pyautogui.locateOnScreen(path_to_screenshots+'Time.JPG', confidence=0.9)
    pyautogui.click(time_button_pos)
    
    pulse_shape_choose_button=pyautogui.locateOnScreen(path_to_screenshots+'Pulse_shape_choose.JPG', confidence=0.9)
    pyautogui.click(pulse_shape_choose_button)
        
    browse_shape_button=pyautogui.locateOnScreen(path_to_screenshots+'Browse.JPG', confidence=0.9)
    pyautogui.click(browse_shape_button)
    
    open_shape_button=pyautogui.locateOnScreen(path_to_screenshots+'Open_pulse.JPG', confidence=0.8)
    pyautogui.click(open_shape_button)
    time.sleep(1) 
    paste(pusle_shape_folder+'In\\'+input_name+'.txt')
    time.sleep(1) 
    pyautogui.press('enter')  

    ok_shape_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Ok.JPG', confidence=0.9)
    pyautogui.click(ok_shape_button_pos)
    
    time_plot_button_pos_1=pyautogui.locateCenterOnScreen(path_to_screenshots+'Time_plot.JPG', confidence=0.9)
    pyautogui.click(time_plot_button_pos_1)
    
    launch_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Launch.JPG', confidence=0.9)
    pyautogui.click(launch_button_pos)
    
    time.sleep(wait_time) 
        
    time_plot_button_pos_2=pyautogui.locateCenterOnScreen(path_to_screenshots+'Time_plot.JPG', confidence=0.9)
    pyautogui.click(time_plot_button_pos_2)
    
    save_plot_button_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'Save.JPG', confidence=0.9)
    pyautogui.click(save_plot_button_pos)
    
    save_plot_button_path_pos=pyautogui.locateCenterOnScreen(path_to_screenshots+'File_name_select.JPG', confidence=0.8)
    pyautogui.click(save_plot_button_path_pos)
    time.sleep(1) 

    paste(pusle_shape_folder+'Out\\'+'Out'+input_name+'.txt')
    
    time.sleep(1) 
    pyautogui.press('enter')  
    
    os.system("TASKKILL /F /IM fresnel.exe")
    time.sleep(3)    
    return()
       
if __name__ == "__main__":
    try:
        os.mkdir(pusle_shape_folder+'In\\')
        os.mkdir(pusle_shape_folder+'Out\\')
    except:
        pass
    
    if clean_start==True:
        if (pyautogui.confirm('All files at '+pusle_shape_folder+'Out\\ will be deleted! Confirm?'))=='Cancel':
            sys.exit(0)
            
        files = glob.glob(pusle_shape_folder+'Out\\*')
        for f in files:
            os.remove(f)
        
    answer=pyautogui.confirm(text='Please choose', title='Choice', buttons=['Single', 'Multiple'])
    if answer=='Single':
        if input_name==False:
            pyautogui.alert(text='No input file name provided! Aborting', title='Error 404', button='OK')
            sys.exit(0)
        if os.path.isfile(pusle_shape_folder+'In\\'+input_name+'.txt') ==False:
            pyautogui.alert(text='File Not Found! Make sure that the input file name is'+input_name+'.txt and it is located in Shapes//In folder!', title='Error 404', button='OK')
            sys.exit(0)            
        if pyautogui.confirm(text='Start calculation for the '+input_name+' file? Output file "Out'+input_name+'.txt" will be created and may overwrite already present file', title='Start', buttons=['Yes', 'No']) == 'Yes':
            generate_one(input_name)
        else:
            pyautogui.alert(text='Ok, then correct the input parameters', title='Error', button='OK')
            sys.exit(0)

    if answer=='Multiple':
        if (pyautogui.confirm(text='Amout of files is '+str(how_much_files)+' and the numeration starts from '+str(start_i), title='Conformation', buttons=['Yes', 'No']))=='Yes':
            generator_many_files(start_i, how_much_files) 
        else:
            pyautogui.alert(text='Ok, then correct the input parameters', title='Error', button='OK')
            sys.exit(0)


        