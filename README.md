
[![LinkedIn][linkedin-shield]][linkedin-url]





<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The programm is created to solve a following task:

Consider having a laser amplification system. The input pulse has relatively small energy, while the output pulse is so powerful that in can damage optical elements.
In such a system, the initial amplification may be simple, but with the energy density increase - the active media saturation happens and the amplification becomes highly non-linear.

In the real experiment, a temporal profile of a laser beam is quite important:
* If present, a pre-pulse may create plasma layer, that will alter the surface interaction with the main pulse.
* The same goes for the beam with a "foot" - i.e. initially weak beam, raising to high energy.
* The most simple and thus desired temporal beam profile - is square.

However, the shape of the input beam, that is needed to receive the square output beam, is unknown. This program aims to solve this problem.


## How the laser is modelled

There are many different software for optical calculations. In this work, [FRESNEL](http://www.wavesimsoft.ru/) is used. 
This program is based on Fresnel diffraction theory, includes all the necessary phenomena like gain saturation, pulse shape distortion etc.

## How the shape is defined

To define the dependence between input and putput beam profiles, Artificial Neural Network (ANN) approach is proposed. 
Input data is used as labels, and output - as training data.
The format of the data can be seen at Shapes folder - it is a simple one-column .txt file. The size is chosen to be 1024 - note that the program will probably not function for other sizes.

## Why automatization is needed

The major problem of ANN creation is need of training dataset. The amount of data should be high for good ANN quality. However FRESNEL doesn't provide the possibility of using random input shapes or any launch automatization - each time the program need to be restarted by hand.
The calculation tume itself depends on the system, beam spatial resolution and the difficulty of the optical scheme. For the 2048x2048 beam size, a scheme containing ~30 optical elements this time typically doesn't exeed 30 seconds.
This means, that to receive a relatively small data amount of 1000, 500 minutes =~ 8 hours of repeated actions is needed.
The automatization comes in handy here, allowing to leave PC for the night and receive the full data set in the morning. 

## How the project is organized

The pjoject contains several files:
* Generation of quasi-random input beam profiles using file RandFuncGen.py
* Performing the opening and necessary manipulations in FRESNEL using Fresnel_automatic.py
* Data load and pre-processing (normalization), and call to ANN using Neural_For_Shape.py
* ANN and several related functions definition using NeuralFunctions.py

## RandFuncGen.py

This file contains several different generators of shapes: 
* random_poly_fit takes a random amount of points (x) and gives them random height (y). Then the points are fit using a polinomial of the random order. All of the random ranges can be modified in the code.
* random_cubic_spline is basically the previous one, but only with a cubic polinomial to fit data. This is used to increase the number of relatively smooth functions in the training.
* random_exponential makes exponentially increasing (with random rate) functions. 
* random_trap makes trapezoidal functions. The two points are defined randomly and then linearly connected.
* random_bragg_like makes a Bragg-like (energy decrease rate of a particle fling through some material) using the increasing function x**(random degree) multiplication on the exponentially decreasing function (random decrease rate).
* rand_func_generator takes all of the previous functions and each call it chooses randomly. Also, it applies gaussian filter with random parameter.

## Fresnel_automatic.py

This script makes use of [PyAutoGui](https://pyautogui.readthedocs.io/en/latest/) library. Basically, this library allows to locate position of preliminary screenshoted items in the screen using cross-corellations.
It also can controll mouse and keyboard - move cursor and click, input text. The latter however causes error when the keyboard laypit differs from English - that is why paste function is introduced.
The script calls for RandFuncGen.py, then opens FRESNEL, set everything up for calculations, including the input of random function location, launches calculation, saves the output. Then it closes and reopens FRESNEL if more files are needed. The reason for reopening - is a major bug in FRESNEL that may result in incorrect data if omit reopening.
## Note that you can't use the PC while the script is running, otherwise Pyautogui may not find the button to push and everything will crash.
The number of files and the wait time before the script think that FRESNEL finished calculations is defined in the beginnig of the file along with all necessary paths.

## Neural_For_Shape.py

This script reads all of the data in the folders, specified in the beginning, loads labels and training datasets in arrays, makes normalization.
An option to compress initial 1024 files is availiable though yet unstable and not recomended for use.
Then the script calls to one of the fuctions of the NeuralFunctions script.


## NeuralFunctions.py
Has several functions:
* train_model - a simple keras ANN is pre-defined and can be changed at will. The model is trained using the pre-defined parameters (that can easily be changed). The model is saved at the dedicated folder.
* optimozer - in comparing with the previous function, this function takes an additional list called parameters as an argument. It uses the values in the list as the amount of neurons in the hidden layer, trains ANN, then tries to receive the desired square function. The ANN's output is loaded into FRESNEL, and the FRESNEL output (typically close to square, but not exactly) is saved in a dedicated folder. This is done to choose the best neuron amount by images comparation.
* additional_training function takes already trained ANN, tries to receive square, but receives something close (quasi-square) and then trains the ANN on this quasisquare and know input. The amount of iterations can be changed.
* plotting function saves the model accuracy curve, and the comparation of predicted by ANN shapes with test and train ones in a dedicated folder. Also, it saves the predicted input to achieve square output in a text file.

## How to use

* Modify Fresnel_automatic, stating the amount of files, correspondong folders, wait time for Fresnel to finish calculations (defined by doing the calculation one time by hand). Launch the script and don't touch the PC intil it's done. In case you want to stop it, pyautogui.FAILSAFE = True is used - moving the mouse cursor to any of 4 angles of the monitor will stop the script.
* Modify NeuralFunctions - the ANN architecture, batch size and epochs amount in both train_model and optimozer functions. Check that the folder are structured like in this GIT project.
* Modify the Neural_For_Shape - change the folders to your data location. Launch Neural_For_Shape and follow printed instructions, choosing which function you want to use. Note, that additional_training can't be launched first as it requires an already trained ANN.  
 

## Notes
_The work is still in progress and some improvements and corrections may be soon done._

## Contact

Iurii Kochetkov -  iu.kochetkov@gmail.com

Project Link: [https://github.com/kofeinix/FRESNEL-auto](https://github.com/kofeinix/FRESNEL-auto)


<!-- MARKDOWN LINKS & IMAGES -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/iu-kochetkov/
