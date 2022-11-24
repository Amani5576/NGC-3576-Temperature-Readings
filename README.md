# Nebula Intensity

Analysing areas of high and low intensity of Statue of Liberty Nebulae based on user specifications.

Data sourced from [this site](https://www.mattdieterich.com/nebuladata "www.mattdieterich.com")  where it was captured from ObsTech in Chile.

## FitExtraction.py file
This file opens and extracts the HDU data from the fit files and puts them into an array; HDUs.
Each fit File consists of a Primary and an Image HDU. These are two sub-lists within each element of HDUs

`HDUs[0]` ---> `[PrimaryHDU, ImageHDU]` from Hydrogen Alpha Fit file
 
`HDUs[1]` ---> `[PrimaryHDU, ImageHDU]` from Oxygen III Fit file
 
`HDUs[2]` ---> `[PrimaryHDU, ImageHDU]` from Silicon II Fit file
     
Hence accessing the `ImageHDU` of in row element `x` of `HDUs` array: 
            
    HDUs[x][1]

Running the file allows you to go through a series of questions to give the necessary information from the header of the Primary such as *Number of data Axes for ImageHDU*, *Approximate right ascension in hours*, *Name of Object*, etc. The file can be run by running python ./FitExtraction.py on any terminal emulator on a computer with Python 3 installed.

## DataAnalysis.py file
This file:
* Closes the Fit files that were opened in the FitsExtraction.py

* Takes the Image HDU data of fit files and puts them in numpy arrays

* Computes Statistical data with regards to pixel numbered values; E.g:
    - Median pixel value
    - Mode(s) of pixel value(s)
    - Standard Deviation of pixel values.
    
* Allows user input in assesment of relative intenisty based on a specific ImageHDU

    -User decides on scaling Factor. For Example:

         You've chosen Scaling factor to be 6 (6 levels of varying intensity):
         
         If max = 80 and min = 20 then range is (80 - 20) = 60
         By dividing the range by the Scale we get -> 60/6 = 10.
         Hence, from Level 1 (highest intensity) to Level 2
         (Second highest intensity) is a difference of 10.
     
    -User decides on the number of level intensities desirable (from highest intesity as the first level)
    For Example:

        Level 1 -> highest intensity level (Thus, type in the integer "1")
        Level 2 -> 2nd highest intensity up until highest intenisty (Thus, type in the integer "2")
        Level 3 -> 3rd highest intensity up until highest intenisty (Thus, type in the integer "3")
        Level 4 -> 4th highest.......etc   
            
    **NOTE**: There automatically exists an initial **level 0**. This intenisty level is only for one value in particular which has the highest intensity value within the *entire matrix*.
             
    *The above essestially decreases processing time if not all intensity levels are desired.*

* Allows user to choose three data ouputs: (which are limited by users chosen Scaling factor)

    -Get pixels that belong to all levels of intensity up until the lowest intensity; then user inputs:
    
    `Yes` *(in order to see all levels)* 
        
    -Get pixels that belong to a particular level of intenisty; then user inputs:
    
    `x` *(`x` is an integer Level number)*
        
    -Let pixels that belong to particular levels of intenisty; then user inputs:
    
    `x,y,z,...` *(multiple integer level numbers of any random chosen level split by commas)*
        
The pixels will be given in terms of a tuple:

    (<x-coord> , <y-coord> , <Intensity_level>)

See image below with an example of chosen user input:

1. Scaling Factor = `40`
2. Level Limit = `10` 
3. Last user input = `yes` 

    
Tuples are used in plotting of filtered data in spectra.py @rofhima13.

For the Hydrogen Alpha Filtered data:

<img src="./img/TupleHA.jpeg">
    
For the Oxygen III Filtered data:

<img src="./img/TupleO3.jpeg">
    
For the Sulphur II Filtered data:

<img src="./img/TupleS2.jpeg">

The file can be run by running python ./DataAnalysis.py on any terminal emulator on a computer with Python 3 installed.

## showSection.py file (by Amani5576)

Used further in Results.py code if user would like to see the Nebula before filtering out the data.
This file shows the initial ImageHDU matrix of each Fit file before any filtration occurs. 
This is due to the fact that each numbered value in the matrices is a quanitity of the number of photons captured by the Telescope. Each element is a pixel containing a specified number of photons.

Choice given for user is only to view one fit file out of the 3 image fit files.
Hence, after running Results, one can still refer back to showSection to reveal the other two.

* For Hydrogen Alpha matrix:

        show(fitFiles[0])  or   show("HA.fits")
    
* For Oxygen III matrix:

        show(fitFiles[1])  or   show("OIII.fits")
    
* For Sulphur 2 matrix:

        show(fitFiles[2])  or   show("SII.fits")

## Results.py file (by Amani5576)

File guides the user to choose between various options of displaying the data:
-Tuples
-Graphs and Pie Charts (Come in unison)
-Tables
-Images
-Combinations of the above
-Special

The "Special" choice allows the user to look at all different layers of a particular matrix. Each layer representing a matrix witht the same size as the original image but with regards to only one intenisty of Photons. (Which can correlate to temperature readings)
Below is an image of the different layers for the Hydrogen Alpha that have significantly noticable differences.

<img src="./img/Layers.png">

The file can be run by running ```python ./Results.py``` on any terminal emulator on a computer with Python 3 installed.
Make sure to run ```pip install -r requirements.txt``` before you run!

Below is a video of the combination of the HA images with regards to the splitting of 100 levels.

https://user-images.githubusercontent.com/110545729/191952049-509730ef-ef19-49ba-b836-2f67241194c0.mp4

Manual code is needed for the superimposition of the dust data onto the stars data like so:

<img src="./img/superimposing.png">