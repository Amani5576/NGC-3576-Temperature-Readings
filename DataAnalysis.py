# Intensity Spectra of Nebulae
# S. Amani Njoroge
# 4060924
# DataAnalysis

from FitsExtraction import HDUs, corrector #importing HDU Data Sets from FIT files as well as copies of the Fit files
import numpy as np #Importing numpy for useful array manipulation.
from statistics import median, multimode, stdev
import sys 

"""
Converting PrimaryHDU's into numpy arrays by firstly extracting them from 
FitsEctract.py package
"""
arrs = [] #Storing numpy matrix of ImageHDU of HA, OIII and SII respetively.
names = ["Hydrogen Alpha", "Oxygen III", "Silicon II"]

for x in range(len(HDUs)):
    #HDUs[x][0] means the Primary HDU whilst HDUs[x][1] would have been ImageHDU
    arrs.append(np.array(HDUs[x][1].data))
    
    #Making sure to close each Fits file after accessing. 
    #Must come after converting the data to numpy array first
    #HDUs[x].close()
    
matrix_title = ["__________________HA array/matrix________________________", "__________________OIII array/matrix_________________________", "__________________SII array/matrix_________________________"]

unfiltMTX = input("""
Show unfiltered matrices of fit file images?

Y/N ?
               
""")
if unfiltMTX == "Y":
    for x in range(len(arrs)): #Looping through length of arrs (starting from 0 to length-1)
        print(matrix_title[x]) #Print the title matrix before printing the matrix data
        print("")
        print(arrs[x]) #Print the matrix 
        print("")
elif unfiltMTX == "N":
    pass
else: 
    corrector()

minToMax_arr = []   #Matrix needed to store 1D data for checking Max and Min 
                    #photons in particular array

#Array storing string elements for ouptutting stat titles
stat_titles = ["_____HA Stats________", "_____OIII Stats________", "_____SII Stats________" ]
max_vals = [] #storing Maximum value of HA, OIII and SII into array, RESPECTIVELY
min_vals = [] #storing Minimum value of HA, OIII and SII into array, RESPECTIVELY
median_arr = [] #storing Median value of HA, OIII and SII into array, RESPECTIVELY
modes_arr = [] #storing Modal(s) value of HA, OIII and SII into array, RESPECTIVELY
stDev_arr = [] #storing standard Deviation value of HA, OIII and SII into array, RESPECTIVELY
    
#Statistical Data
statDats = input("""
Print statistical Data outputs of each fit file? 

Y/N ?

""")
    
for x in range(len(stat_titles)):
    for i in arrs[x]: #Looping over each individual sub-araay list
        for j in i: #Looping through each element in specific sub-array list
            minToMax_arr.append(j) #Adding each element into 1D array 
    minToMax_arr.sort() #Sorts the array in ascending order
    maxim, minim = minToMax_arr[-1], minToMax_arr[0]
    up_q, low_q = np.percentile(arrs[x],75), np.percentile(arrs[x],25) #getting upper and lower quartile of each matrix data
    med =  median(minToMax_arr)
    median_arr.append(med)
    mode = multimode(minToMax_arr)
    modes_arr.append(mode)
    mean = np.mean(arrs[x])
    std = stdev(minToMax_arr, xbar = mean)
    stDev_arr.append(std)
    max_vals.append(maxim)
    min_vals.append(minim)
    minToMax_arr.clear() #Clearing array of all content for OIII and SII data storing
    if statDats == "Y":
        print(stat_titles[x]) #print the current stat title
        print("")
        print("Maximum photons in a pixel = ", maxim) #Max pixel value
        print("Minimum photons in a pixel = ", minim) #Min Pixel value
        print("Upper quartile = ", up_q) #Printing upper quartile info
        print("Lower Quartile = ", low_q) #Printing lower quartile info
        print("Median = ", med) #Getting median value
        print("Mode(s) = ", mode) #Getting modal value. Using multimode in case of two modes or more
        print("mean= %.3f " % mean)
        print("StDev = ", std) #Standard Deviation
        print("")
    elif statDats == "N":
        pass
    else: 
        corrector()
    
###############################################################################
"""
Below is the part where I Look at levels of high to relatively low intensity
The levels of intensity will be rated by the maximum and minimum values that
were previously collected.

All other lower levels of intensity are counted as negligible if user chooses 
a number of levels.

By increasing the scaling factor, the data is categorized in more levels.
By inputting the number of levels (starting from the highest level; Level 1), 
the data recorded will be categorized upto that level.
"""
###############################################################################
print("_______________________________________________________________________________________________")

# Limitation based on Colour of an object in digital systems
maxColor = 2**8-1 #0 -> 255

#Creating user-input based Scale-Levels for relative intensity
scF = int(input("""
                           
Please input the number of levels.
            
Its advisable to choose a high number such as %d or higher.
Highest value to be chosen is %d due to a limitation of 
Colour of an object in digital systems.

     
""" % (int(maxColor/4),maxColor)))

Levels = int(input("""
Levels have been successfully constructed. 

Note: Highest intesity level = 1
      Lowest intesity level = %d
                                  
Are you sure you want all the data to be processed and inputted till level %d?
If so, then type %d again. 
        
Input the number of level intensities you desire.
(e.g. if you type 6, data will process from level 1 to 6)
Recommended to choose upto the top quarter tier level such as level %d or lower. .
(Warning: can take longer depending on processessing power of your device)     

""" % (scF,scF,scF,int(scF/4))))

print("_______________________________________________________________________________________________")
print("")

if scF > maxColor: #If the chosen number of levels are bigger than the Scaling Factor:
    print("""
          You have split the data into %d levels but the limitation (based on 2D pixel data) is %d in length/width. 
          """ % (scF, maxColor))

    sys.exit("Please rerun the code an choose wisely.") #exiting the code with a message if the preceeding if statement is met

if Levels > scF: #If the chosen number of levels are bigger than the Scaling Factor:
    print("""You have split the data into %d levels but have chosen your levels of interests to level %d. 
          """ % (scF, Levels))

    sys.exit("Please rerun the code and choose wisely.") #exiting the code with a message if the preceeding if statement is met
         
scales = [] #Array holding constructed scales for HA, OIII and SII

for x in range(len(max_vals)):
    scales.append((max_vals[x] - min_vals[x])/scF)

XYm_gList = [] #List that holds tuples of (x,y,intensity level) for g_arr
XYm_hList = [] #List that holds tuples of (x,y,intensity level) for h_arr
XYm_iList = [] #List that holds tuples of (x,y,intensity level) for i_arr

#array containing all XY_()List
XYm_Lists = [XYm_gList, XYm_hList, XYm_iList]

for q in range(len(XYm_Lists)): #Sorting/Categorising levels.
    i_idxNum = 0 #Index number
    for i in arrs[q]: #Looping through array of HA, then OIII then SII
        y = i_idxNum #row number or y coordinate of element
        j_idxNum = 0 #column number
        for j in i: #for every element in the list "i"
            mltp = 0 #creating multiplier variable
            x = j_idxNum #column number or x coordinate of element
            while mltp <= scF and mltp<=Levels+1: #If the multiplier vairable smaller than or equal to the scaling factor
                                                  #Also making sure to dump the rest of the other data inside an extra lower level
                if j >= max_vals[q] - mltp*scales[q]: 
                    """Checking condition if data is in specific intensity level 
                    in terms of the pixel's photon number. First level is from maximum (inclusive)
                    to lower region of that first level (also inclusive)"""
                    if mltp == Levels+1 or (x,y,mltp-1) in XYm_Lists[q]: #If data lands in extra level or if coordinate already exists
                        break #Get out of while loop rather than recording it
                    else:
                        temp_tup = (x,y,mltp) #Trapping tuple of coords and their corresponding multiplier
                        #tuples t in (<x>,<y>, t) where t = 0 are just the pixel coordinates that have maximum number of photons.
                        XYm_Lists[q].append(temp_tup) #Tuple will be having cooridnate elements x, y as well as the reverse multiplier prescribed to that coordinate.
                mltp += 1  #Increasing multiplier to find the next relative intensity
            j_idxNum += 1 #Incrementing the x-cooordinate
        i_idxNum += 1 #Incrementing the y-coordinate
    #Sorting all tuple elements in the List array
    XYm_Lists[q].sort() #Sorting list in ascending order