# Intensity Spectra of Nebulae
# Samwel Amani Njoroge
# 4060924


# Importing arrays (arrs -> images, levels -> user input, XYm_Lists -> filtered images)

from FitsExtraction import agree, disagree, corrector
from DataAnalysis import get_coords, get_z_axis_max, tick_sizes, plot_contour_3d_graph, plot_3d_Dust, get_z_axis_min #FUNCTIONS
from DataAnalysis import XYm_Lists, XYm_types, Levels, names, arrs, stat_data, prop, sum_for_prop #VARIABLES
import matplotlib.pyplot as plt # Import matplotlib library for plotting
import matplotlib.colors as col # Import matplotlib library for color mapping
from scipy.stats import norm #getting norm to gain probability density function
from tabulate import tabulate as tb
from scipy.optimize import curve_fit
from math import floor, log10
import numpy as np # Import numpy library for array arithmetic
import showSection as ss
import csv

min_vals, max_vals, stDev_arr, median_arr, modes_arr, up_q_arr, low_q_arr = stat_data

#Redefining function name for simpler analogy
plot_combined = plot_3d_Dust

#Filters lists by removing unwanted tuples based on chosen level from user input
#levelFilter returns a filtered out (or shortened) list of tuples
def levelFilter(tuplist, d): 
    templist= []
  
    #If the level given is only an integer value of a specific level
    if type(d) == int: 
            for tup in tuplist: #For each tuple within the list
                if tup[2] == d: #if the intesity level within tuple is equal to desired user input
                    templist.append(tup) #Add tuple element into temporary list
                    
    #If the level given is an array of specifically chosen levels
    elif type(d) == list:
            for tup in tuplist: #For each tuple within the list
                for h in d: #For each level of interest given by user
                    if tup[2] == h: #if the intesity level within tuple is equal to desired user input
                        templist.append(tup) #Add tuple element into temporary list
                        break #Stop checking current tuple, move to next one.
    
    #If they typed "all" or "Yes"
    elif type(d) == str: 
        templist = tuplist #No filtering to be done
        
    return templist

def sigfig_1(x): #Function that converts uncertianties to significant figure
#Function is used in other function 'sigdigits()'

    if type(x) == int or type(x) == float:
        a = -int(floor(log10(abs(x))))
        #Retirved form this site: 
        #https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python

        return round(x,a)
    
    else:
        x = np.array(x)
        a = np.floor(np.log10(abs(x)))

        for ind,x1 in enumerate(a): #Going over list
            if abs(x1) == np.inf: #If infinity is within the list
                a[ind] = 0 #Convert infinity to 0
        a = [-int(num) for num in a]

        x = list(x)
        a = list(a)
        for ind,f in enumerate(x):
            x[ind] = round(f,a[ind])
        return x
    
def rounder(val,unc): #Rounds value based on its corresponding uncertainty
    length = len(str(unc)) #getting length of uncertainty
    val = round(val,-(length-1))
    
    return val

def gauss(x,A,mu,sig): #Creating Gaussian function
        a = A*np.exp(-(x-mu)**2/sig**2)
        return a
        
def specify_levels(choice): #Converts user input to appropriate type, list
                
        #NOTE: 'choice' variable is only a string and needs to be converted for proper usage:
        numbers = [str(i) for i in range(10)] #array of unit numbers as strings
        if "," in choice: #If multitude of specific levels are chosen
            #Convert choice string input into list of those specific levels
            f = choice.split(",") #Automatically splits every string element based on the specified arguement splitter
            #f is an array of strings with each string being a level number
            d = [] #Element to store integer values
            for i in f: #Converting every string element into an integer
                d.append(int(i)) #adding integer version of each number string into new list
        #if the input was only of one level
        elif "," not in choice and choice[0] in numbers and ":" not in choice: 
            d = int(choice) #Convert level from string to integer
        elif ":" in choice: 
            d = [] #Element to store range of level choices
            ind = choice.index(":")
            for i in range(int(choice[:ind]),int(choice[ind+1:])+1): #starting from n ending at m where [n:m] where "m' is included
                d.append(i)
        else: 
            d = choice #Remains as string
            
        return d
    
def viewing(): #Getting users preference in what type of data to produce
    
    ViewingChoices = ["T","G","TB","I", "A","3D","PF"]
    
    ViewChosen = input("""
                       
Desired output:
    
*Tuples of coorindate data?  -> T
(Printing Tuples might take some time)

*Graphs and Pie Charts -> Then type G

*Tables -> TB

*Images -> I

*A Combination. E.g Graphs and Pie Charts, Images and Tuples-> G,I,T

*All the above? -> Then Type the Letter A

*3D Graphing of chosen layers -> 3D

*PixelFrames: -> Type the word: PF
(Printing filtered image of each intenisty level seperately)

""")#PixelFrame prints all layers one by one from highest pixel images upto lowest
    print("---------------------------------------------------------")
    print()
    
    #Convert choice inputs into list array of those choices (if there are more than one)
    if ',' in ViewChosen:
        ViewChosen = ViewChosen.split(",") #Automatically splits every string element based on the specified arguement splitter
        #Overwriting "x" with its new list-form rather than remaining as string.

    if type(ViewChosen) == str: #If singular invalid choice made
        if ViewChosen.upper() not in ViewingChoices: 
            print("%s was not one of the options" % ViewChosen)
            corrector()
    else: #If a list of choices were made with invalid inputs
        for i in ViewChosen:
            if i not in ViewingChoices:
                corrector()
        if ("A" in ViewChosen and "PF" in ViewChosen) or ("A" in ViewChosen and "3D" in ViewChosen) or ("3D" in ViewChosen and "PF" in ViewChosen):
            print("PixelFrames and 3D can only be chosen individually")
            corrector()
    
    return ViewingChoices, ViewChosen

#Returns list for stored tuples based on proceeding filtration system; 'levelFilter'
def filtered_arrs(**kwargs):

    filt_tuple_lists = [] 
    arrs = []
    
    for k,v in kwargs.items():
        if k == 'multiple' and v == True:
            #Looping through 3 groups of filtered tuple (HA, OIII and SII)
            for i in range(3):
                if i == 0: #If dealing with hydrogen Alpha
                    d = kwargs['HA'] #Take users choice(s) of HA level(s)
                    filt_tuple_lists.append(levelFilter(XYm_Lists[i], d)) #Filtering the data
                    
                if i == 1: #If dealing with Oxygen 3
                    d = kwargs['O_3'] #Take users choice(s) of HA level(s)
                    filt_tuple_lists.append(levelFilter(XYm_Lists[i], d)) #Filtering the data
                    
                if i == 2: #If dealing with Sulphur 2
                    d = kwargs['S_2'] #Take users choice(s) of HA level(s)
                    filt_tuple_lists.append(levelFilter(XYm_Lists[i], d)) #Filtering the data
                    
                #Where all-else will be assigned a value -1
                for filt_tuple_list in filt_tuple_lists: 
                    # Create a 400x400 matrix filled with range outside maximum intensity (Level 0)
                    arr = np.zeros((400,400), dtype = int)
                    
                    for ind_1, a_1 in enumerate(arr):
                        for ind_2, a_2 in enumerate(a_1):
                            arr[ind_1,ind_2] = -1
                            
                    for coord in filt_tuple_list:
                        #Making an imprint of an existing pixel in empty arr-matrix
                        #Based on tuple information in 'filt_tuple_list'
                        arr[coord[1], coord[0]] = coord[2]
                        
                arrs.append(arr) #Add filtered matrix (for 3d graphs) into arrs list 
        
        elif k == 'multiple' and v == False:
            #Looping through 3 groups of filtered tuple (HA, OIII and SII)
            for i in range(3):
            
                filt_tuple_lists.append(levelFilter(XYm_Lists[i], kwargs['d'])) #Filtering the data
                
                #Where all-else will be assigned a value -1
                for filt_tuple_list in filt_tuple_lists: 
                    # Create a 400x400 matrix filled with range outside maximum intensity (Level 0)
                    arr = np.zeros((400,400), dtype = int)
                    
                    for ind_1, a_1 in enumerate(arr):
                        for ind_2, a_2 in enumerate(a_1):
                            arr[ind_1,ind_2] = -1
                            
                    for coord in filt_tuple_list:
                        #Making an imprint of an existing pixel in empty arr-matrix
                        #Based on tuple information in 'filt_tuple_list'
                        arr[coord[1], coord[0]] = coord[2]
        
                arrs.append(arr) #Add filtered matrix (for 3d graphs) into arrs list 
        
    return arrs

def csv_export_query():
    outfileOpt_1 = input("""
    Copy HA, OIII and SII Tuples into rows within a csv file, repsectively?

    Y/N ?

    """)

    fieldnames = ['X','Y','m']

    #Taking all raw tuples from XYm_types and saving them in csv file
    if outfileOpt_1.lower() in agree:
        
        for j in range(len(XYm_types)):
            file = open(XYm_types[j] + ".csv", "w")  # 'w' means write
            
            writer = csv.DictWriter(file, fieldnames) #Treat file as a csv file (commer seperated values)
            writer.writeheader()
            
            for i in XYm_Lists[j]: #Loop through the the current list of tuples. types: HA, OIII and SII
                writer.writerow({'X': i[0], 'Y': i[1], 'm': i[2]}) #Log in the x coords, y coords and magnitude
            
        file.close() #Once all csv writing is done, close the file
    elif outfileOpt_1.lower() in disagree:
        pass
    else:
        corrector()
        
def showUnfilt_query():
    showUnfilt = input("""
    Would you first like to see what the Nebula looks like before it had been filtered?

    Y/N?

    """)
          
    if showUnfilt.lower() in agree:
        unfiltImg = input("""
    Which one would you like to see?
        
    Hydrogen Alpha? Type 0
    Oxygen 3? Type 1
    Sulphur 2? Type 2
        
    All the above? type all

    """)
              
        p = ".fit"
        if unfiltImg == "0":
            ss.show("HA" + p)
        elif unfiltImg == "1":
            ss.show("OIII" + p)
        elif unfiltImg == "2":
            ss.show("SII" + p)
        elif unfiltImg == "all":
            ss.show("HA" + p)
            ss.show("OIII" + p)
            ss.show("SII" + p)
        else:
            corrector()    
    elif showUnfilt.lower() in disagree:
        pass
    else: 
        corrector()
    
def print_filt_layers(): #printing images layer by layer of intensities
    
    choice = input("""

Printing filtered image of each intenisty level seperately:

Which images to produce  ->  Type The nubmer:
-----------------------------
     HA                  ->        0
    OIII                 ->        1
     SII                 ->        2
________________________________________________

choice? """)
    
    if choice in [str(i) for i in range(3)]: #If collage choice is valid
        for i in range(3): #Looping through length of collage chosen (in this case just 3)
            if int(choice) == i: #If integer collage chosen is equal to the current i value
                filt = [] #Creating list for storing filtered lists Data
                for num in range(Levels+1):
                    d = num
                    filt = levelFilter(XYm_Lists[i], d) #Filtering the data
                    arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
                    for coord in filt:
                        #Making an imprint of an existing pixel in current level
                        arr[coord[1], coord[0]] = 1 
                    plt.xlabel("Image X-axis")
                    plt.ylabel("Image Y-axis")
                    plt.title("%s (lvl %d)" % (names[i],d))
                    plt.axis('off')
                    plt.imshow(arr, cmap=plt.cm.gray)
                    plt.figure() # Show plot in its own windowclear
                    plt.show()
    else:
        corrector()
    
def print_tuple_data(ViewChosen, names, Levels, XYm_Lists, filt, d, choice):
    if Levels !=1:
        if ViewChosen == "T" or ViewChosen == "A": 

            print("NOTE: data output will be given as: ( <x-coord> , <y-coord> , <Intensity level> )")
            print()
            print("If <Intensity level> = 0, then this is the only pixel in the matrix that has the largest number of photons")
            print()
            
            for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
                
                #If the current data is of empty list
                if XYm_Lists[x] == []:
                    print("Coordinates of %s from intensity Level 1 -> %d:" % (names[x],Levels))
                    print()
                    print("There are no intenisties within Level 1 -> %d for %s" %(Levels, names[x]))
                    print()
                    
                #if the input is "yes" or "all"
                if type(d) == str:#Making sure its not case sensitive by just checking if its a string
                    print("Coordinates of %s from intensity Level 1 -> %d:" % (names[x],Levels))
                    print()
                    print(XYm_Lists[x]) #Print the list of tuples
                    print()
                
                else: #If user input was a specific level or a multitude of levels
                    print("Coordinates of %s in levels %s data:" % (names[x],choice))
                    print()
                    print(filt) #printing out filtered tuples
                    print()
    else:
        if ViewChosen == "T" or ViewChosen == "A": #If user want to see tuple data
            for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
                print("Coordinates of %s from intensity Level 1:" % (names[x]))
                print()
                print(XYm_Lists[x]) #Print the list of tuples
                print()
     
def graphing_3d_query():
    
    typ = int(input("""
Choose from below:

    Hydrogen Alpha -> type the number 1
    Oxygen III     -> type the number 2
    Silicon II     -> type the number 3 
    All together   -> type the nubmer 4

""")) - 1

    if type(typ) != int:
        print("Please retry again making sure your choice begins and ends with a number")
        print()
        typ = graphing_3d_query()
    
    return typ

def get_user_custom_levels():
    choice = input("""
                               
Would you like to see all levels from highest to lowest level ? If so type 'yes' or 'all'

Or 

Type an integer to see only one level number:
    
Or

Would you rather specific levels (more than one)? 
    e.g: Only want pixel coordinate with the highest value: type -> 0
         Only level 2 and level 3: then type -> 2,3
         Only Level 6 and level 31 and level 4: then type -> 6, 31 , 4
         (spacing doesnt matter, but make sure to separate using commas)
         A range from 4 to 50: then type -> 4:50
                 
                    """)
    print("---------------------------------------------------------")
    print()
    
    if choice == 'yes' and 'choice' != 'all':
        pass
    else: 
        try:
            #If first and last input are numbers
            if int(choice[0]) in range(Levels) and int(choice[-1]) in range(Levels)  : 
                pass #Move on to next part of code
        except ValueError: #invalid literal for int()
            print("Please retry again making sure your choice begins and ends with a number")
            print()
            choice = get_user_custom_levels() #Go through function again
        
    return choice
    
def KDE_3d_Contour_combined_query():
    print("""

Follow one of the options per each of the following choices afterwards

    1.) Input specific levels with either range n:m where n&m are integers where n<m
    
    2.) Seprate individual choices with commas e.g. 1, 2, 3, if more than one
    
    3.) Press enter to skip dataset 

""")

    a = []
    p = ["80:84", "80:90", "99"]
    for i, name in enumerate(names):
        # a.append(input("""Which specific levels of %s? """ % name))
        a.append(p[i])
        if a[i] == "": #If user skipped it with an enter
            #making 'dummy' array in order for it to be ignored due to being smaller than 0
            a[i] = np.array([[1]*400, [1]*400, [1]*400])*-1
        
        try:
            #If first and last input are numbers
            if int(a[i][0]) in range(Levels) and int(a[i][-1]) in range(Levels)  : 
                a[i] = specify_levels(a[i])
        except ValueError: #invalid literal for int()
            print("Please retry again making sure your choice begins and ends with a number")
            print()
            a = KDE_3d_Contour_combined_query() #Go through function again and overwrite the array 'a'
            break #Get out of for loop to not overwrite users correct inputs
            
    return a
    
    
def main(arrs):
    
    csv_export_query()
           
    showUnfilt_query()
   
    ViewingChoices, ViewChosen = viewing()
    
     
    if ViewChosen.lower() == "pf": #printing Filters layer by layer
        print_filt_layers()
        
    #If its a list of other choices that isnt "PF" or '3D'
    elif type(ViewChosen) == list: 
        
        #Checking if list of choices only has valid inputs
        for i in ViewChosen: #Looping thorugh all choices
            if i not in ViewingChoices: #If the user input is invalid
                corrector()
                
        filt = [] #Creating list for storing filtered XYm_Lists Data

        #Note that input() automatically converts user intput into a string
        if Levels !=1: #If there is more than just one level
            
            choice = get_user_custom_levels() #Chocie in form of a string
            
            d = specify_levels(choice) #Convert string choices into correct datatype and/range
                
            #______________________________________________________________________________________________________________
            
            for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
                #function filters lists by removing unwanted tuples based on chosen level from user input
                filt.append(levelFilter(XYm_Lists[x], d)) #levelFilter returns a filtered out (or shortened) list of tuples
            #______________________________________________________________________________________________________________
            
            
            #Printing of Tuple Data of coordinates when Levels constructed are more than one
            print_tuple_data(ViewChosen, names, Levels, XYm_Lists, filt, d, choice)
     
        else: #Printing of Tuple Data of coordinates with no constructed levels. (Only just Level 1) 
            print_tuple_data(ViewChosen, names, Levels, XYm_Lists, filt, d, choice)

        # def plot_spectrum(x): # Create a function to plot the spectrum
        #     pixels = np.mean(x, axis=1) # Get average of all pixels relative to x-axis
        #     # Plot the resultant spectrum
        #     plt.plot(range(len(pixels)), pixels)
        #     plt.xlabel("Pixel Number (relative to x-axis)")
        #     plt.ylabel("Light Intensity relative to x-axis (Arbitrary Unit)")

        # for file in arrs:
        #     plot_spectrum(file)
        # plt.title(f"Intensity Spectrum of Nebulae") # Title of the plot for all nebulae
        # plt.legend(names) # Legend of the plot
        # plt.figure() # Show plot in its own window


        #______________UQ, Median and LQ Data for all fit files___________________
        if "G" in ViewChosen:
            plt.minorticks_on() #Switching on the minor gridlines         
            plt.figure(1)
            plt.grid(visible = True, which="both" , axis="y" , color = "grey")
            flat = [] #Stores 2D data of HA file into 1D
            for i, file in enumerate(arrs):
                flat.append(file.flatten())
            plt.ylabel("Photpix")
            plt.boxplot(flat, labels = names)

        #______________UQ, Median and LQ Data for O III___________________
            plt.figure(2)
            plt.grid(visible = True, which="both" , axis="y" , color = "grey")
            plt.minorticks_on() #Switching on the minor gridlines 
            flat = [] #Stores 2D data of HA file into 1D
            flat.append((arrs[1]).flatten())
            plt.ylabel("Photpix")
            plt.boxplot(flat, labels = [names[1]])
            #names[1] is in array otherwise the boxplot reads each character of letter as an individual x component of the graph
            
            
        #______________UQ, Median and LQ Data for SII___________________
            plt.figure(3)
            plt.grid(visible = True, which="both" , axis="y" , color = "grey")
            plt.minorticks_on() #Switching on the minor gridlines 
            flat = [] #Stores 2D data of HA file into 1D
            flat.append(arrs[2].flatten())
            plt.ylabel("Photpix")
            plt.boxplot(flat, labels = [names[2]])
            
        #____________________Filtered Images__________________________________________________________________
        
        # Create a 400x400 matrix of zeros for HA, OIII and SII
        arr = [[],[],[]]
        for i in range(3):
            arr[i] = np.zeros([400,400]) 
        
        #Putting filtered data into zero matices
        for i,data in enumerate(filt):
            for tupl in data: # Loops through each of the filtered data, plots accordingly
                arr[i][tupl[1], tupl[0]] = 1 # creating the filtered version of the original matrix
                # (Max = Levels - 0, where 0 -> Max intensity)
            
            if "I" in ViewChosen: #If user asked for Image Display of new filtered matrix
                plt.imshow(arr[i], cmap=plt.cm.gray)
                plt.xlabel("Image X-axis")
                plt.ylabel("Image Y-axis")
                plt.title("%s" % names[i])
                plt.axis('off')
                plt.figure() # Show plot in its own window
                plt.show()
                plt.clf()
        
        dust = arr[1]*200 + arr[2]*130 #Matrix of dust
        #Amplification of OIII dust by multiplying it by 50
        starDust = dust + arr[0]*255 #Matrix of star formation and Dust
        #Amplification of HA by multiplying it by 100
        
        #Defining my own special color map:
        amani_map1 = col.ListedColormap(["black","yellow","red"])
        amani_map2 = col.ListedColormap(["black","blue","yellow","red"])
        
        if "I" in ViewChosen: #If user asked for Image Display of new filtered matrix
            plt.figure(4) # Show plot in its own window
            plt.imshow(dust, cmap = amani_map1)
            plt.xlabel("Column number")
            plt.ylabel("Row number")
            plt.axis()
            cbar1 = plt.colorbar(orientation = "vertical", shrink = 0.5)
            cbar1.set_ticks([65,165,270])
            cbar1.set_ticklabels(["No Dust","Sulphur","Oxygen"])
            
            plt.figure(5) # Show plot in its own window
            plt.imshow(starDust, cmap=amani_map2)
            plt.xlabel("Column number")
            plt.ylabel("Row number")
            plt.axis()
            cbar1 = plt.colorbar(orientation = "vertical", shrink = 0.8)
            cbar1.set_ticks([73.125,73.125*3,73.125*5,73.125*7])
            cbar1.set_ticklabels(["Vaccum","Hydrogen (lvl 0 - 82)","Sulphur (lvl 99)","Oxygen (lvl 98)"])
            plt.show()
            
        
                # plot_spectrum(arr.transpose())
                # plt.title(f"Filtered spectrum data for {names[i]}")
                # plt.figure() # Show plot in its own window
        
        #__________Histograms_________________________________________________________________________
        domain = range(min_vals[0],max_vals[0],1) #Domain is from minimum to maximum of  Photpix of HA
        step = 2
        binRange = np.arange(domain[0], domain[-1], step) #binwidth of histograms

        
        plt.figure(6) #Figure 1 is for 1st histogram
        hist1 = plt.hist(arrs[0].flatten(), bins = binRange, density = False, rwidth=0.5) #Creating histogram 1
        plt.xlabel("Photpix", size = 13)
        plt.ylabel("Number of Pixels", size = 13)
        
        
        if "G" in ViewChosen:
            plt.figure(7)
            
            #plotting histogram
            plt.hist(arrs[0].flatten(), bins = binRange,density = True, rwidth=0.5) #Creating histogram 2
            
            #Creating normalised version of graph
            plt.plot(domain, norm.pdf(domain,np.mean(arrs[0]),stDev_arr[0]),label = "Estimate probability curve", c= "black")
            plt.ylabel("Normalised Number of Pixels", size = 13)
            plt.xlabel("Photpix", size = 13)
            plt.legend()
        
        #GAUSSIAN________________________________________________________________________
        
        #Taking subset of the Data
            yVals , xVals = list(hist1[0]) , list(hist1[1]) #Converting numpy array to list
            
            x_dats = xVals[xVals.index(39):xVals.index(85)] #(From 42 to 84 )
            y_dats = yVals[xVals.index(39):xVals.index(85)]
                 
            #popt -> Gives optimal parametres that make the gaussian curve best fit the data points
            #pcov -> Covariance matrix giving estimate of errors
            
            #NOTE: Gaussian Function as a function
                #gauss(x,A,mu,sig)
                #A = Amplitude (Guessing it to be 7500)
                #mu = Centre of the graph (Guessing the value 59)
                #sig = Sigma is about 10 (assumption)
                
            popt , pcov = curve_fit(gauss, x_dats, y_dats, p0=[7500,60,10])
            
            A_opt, mu_opt, sig_opt = popt 
            
            # A_opt -> Optimal value for A
            # mu_opt -> Optimal value for mu
            # sig_opt -> Optimal value for sig
            
            x_fit = np.linspace(0,xVals[-1],1000) # x coords for Gaussian fit
            y_fit = gauss(x_fit, A_opt, mu_opt, sig_opt) # y coords of Gaussian fit
            
            Unc_mu = np.diag(pcov)[1] #Uncertianty in the peak value of mu
            percUnc_mu = (Unc_mu/mu_opt)*100 #Percetnage uncertanty of Mu
            
            
            plt.figure(9)
            plt.minorticks_on()
            plt.grid(visible = True, which="both" , axis="both" , color = "grey")
            plt.xlabel("Photpix", size = 13)
            plt.ylabel("Number of Pixels", size = 13)
            plt.scatter(xVals[:-1],yVals, label = "Grouped data Points from Histogram")
            plt.plot(x_fit,y_fit,color = "blue", label = "Gaussian Fit")
            plt.legend()
            
            plt.figure(10)
            plt.minorticks_on()
            plt.grid(visible = True, which="both" , axis="both" , color = "grey")
            plt.xlabel("Photpix", size = 13)
            plt.ylabel("Number of Pixels", size = 13)
            plt.scatter(x_dats,y_dats, label = "subset of Grouped data Points from Histogram")
            plt.plot(x_fit[148:370],y_fit[148:370],color = "blue", label = "Gaussian Fit")
            plt.legend()
            
        else: #Do not show histograms
            plt.close(6)
            plt.close(7)

        #_________Table 1_____________

        # #Shortnening the table`
        # zipped = list(zipped)
        # for ind,x in enumerate(zipped):
        #     if ind%2 != 0: #If the index number is odd
        #         zipped.pop(ind)

        #Use of Wien's displacement law
        b = 2897771.955 #Wien's displacement constant in nm Kelvins
        lmbd = 656.281 #wavelength of H_A emission line in nm
        Temp = b/lmbd  #Temperature of HA in Kelvin
        ratio = Temp/mu_opt #Ratio between maximum average Photopix (from histogram) and Temperature of HA wavelength (from Weins law).
        Temps = [] #Stores all corresponding temperatures based on the ratio of highest peak to the Temperature
        Unc_Temps = [] #Stores all corresponding uncertainties of temperatures based on the ratio of highest peak to the Temperature

        tempHist = hist1[1]+round((step/2),1)
        tempHist = tempHist.round() #Rounding off due to photons conceptually being a whole rather than a fraction
        
        for x in tempHist: #Converting average bin of histogram photopix to temperature.
            a = round(ratio*x,3)
            a_unc = a*(percUnc_mu/100)
            a_unc = sigfig_1(float(a_unc)) #Converting uncertainry to 1 significant figure
            a = rounder(a, int(a_unc)) #Rounding off Temp value based on rounded uncertainty
            Temps.append(int(a))
            Unc_Temps.append(a_unc)
            
        titles = ["Photpix","No. of Pixels","Temp(K)", "d Temp (K)"] #Headers for table
        zipped = zip(tempHist,hist1[0],Temps,Unc_Temps) #Zipping up each coordiate into tuples
        Zip = list(zipped) #Used in creation of smaller tables
        table1 = tb(Zip,headers = titles) #creating table 
        if "TB" in ViewChosen or "A" in ViewChosen:
            print(table1)

        #_________Pie Chart 1 (On All Temperatures)_____________

        if "G" in ViewChosen:
            exploders = [] #Storing exploders for pie chart.
            for x in hist1[1]: #Looping through PhotPix within table 1
             #Aids in making the pie chart a bit more readerable
                exploder = 0
                n = 25
                for f in range(1,int((250/n))):
                    if x > max(hist1[1]) - (f*n):
                        exploders.append(round(exploder,1)) #adding exploder values into exploders list
                        break
                    else: 
                        exploder += 0.2
            plt.figure(11)
            # plt.title("Distribution of All Temperatures in NGC 3576")
            exploders.reverse()
            plt.pie(hist1[0], labels = Temps[:-1], explode = exploders[:-1], textprops={'fontsize': 8})
            
            
        #_________Segregation of temperatures_____________
        
        gulp = []
        for i in exploders:
            if i in gulp:
                pass
            else:
                gulp.append(i)
        
        mag_Temps = []
        seg_zips = []
        LtoS = []
        for i in range(len(gulp)):
            mag_Temps.append([]) #Based on thier magnitude
            seg_zips.append([]) #Based on magnitude of Temperatuers
            LtoS.append("Group " + str(i+1))
            
            
        #Getting splitting constant for segregation
        seg_cons = (max(Temps) - min(Temps))/8

        for ind,x in enumerate(mag_Temps):
            for y in Temps:#Looping through each Temperature value.
                if (max(Temps) - seg_cons*(ind)) >= y > (max(Temps) - seg_cons*(ind+1)):
                    x.append(y)

        #__________Segregation of zipped tuples_________________________

        
        for x in Zip:
            for j,y in enumerate(mag_Temps):
                for y1 in y:
                    if x[2] == y1:
                        seg_zips[j].append(x)

        #_________Smaller(Temp-segragated) Tables_____________

        for i in seg_zips:
            table = tb(i,headers = titles) #creating table 
            if "TB" in ViewChosen or "A" in ViewChosen:
                print(table)
            
        #________________Other Pie Charts_________________

        if "G" in ViewChosen:

            for x in range(len(seg_zips)): #Looping through number of elements in seg_zips
                
                # *a makes the array "a" appear wihtout its outer brackets.
                newList = list(zip(*seg_zips[x])) #Unzipping
                
                plt.figure(12+x)
                plt.title("Distribution of %s Temperatures (in K)" % LtoS[x])
                plt.pie(newList[1], labels = newList[2])
                #newList[2] = Relative Temperatures
                #newList[1] = Relative Number of Pixels
                
        #_________Tables of Statistical Data________________
            
        subTitles = ["St. Dev.", "Min", "Max", "Median", "Mode", "Up Q","Low Q"]
        zipped = zip(names, stDev_arr, min_vals, max_vals, median_arr, modes_arr, up_q_arr, low_q_arr)
        Zip = list(zipped) #Used in creation of smaller tables
        table2 = tb(Zip,headers = subTitles) #creating table 
        if "TB" in ViewChosen or "A" in ViewChosen:
            print(table2)
                
         
    #     #_______________________Counting pixels that are not 0_____________________________

    #     print()
    #     print("_____Number of non-zero Pixels______")
    #     print()
    #     notE = []
    #     for i in range(len(names)):
    #         counter = 0
    #         countArray = []
    #         for ox in arr[i]:
    #             counter = list(ox).count(0)
    #             countArray.append(counter)

    #         notempty = len(arr[i])**2 - sum(countArray)
    #         notE.append(notempty)
    #         print(names[i], " = ", notE[i])
        
    #     dust = arr[1]+arr[2]
    #     countArray = []
    #     for d in dust:
    #         counter = list(d).count(0)
    #         countArray.append(counter)
    #     notempty = len(arr[i])**2 - sum(countArray)
    #     print()
    #     print("Number of Dust pixels = ", notempty)

    if ViewChosen.lower() == '3d':
        
        typ =  graphing_3d_query()
        
        #If keeping 3d graphs of HA, OIII and SII separate
        if type(typ) in range(3):
            
            choice = get_user_custom_levels()
            
            d = specify_levels(choice) #'d' variable needed within the levelFilter function
            
            arrs = filtered_arrs()    
            
            if typ in [0,1,2]: #If input of the user was valid
            
                X, Y, Z = get_coords(max_x = 400, max_y = 400, groupedIMGArray = arrs, arrayNum = typ, multiple = False)
                #arrayNum = 1 -> OIII data
                #arrayNum = 0 -> HA data
                #arrayNum = 2 -> SII data
                                #Scale is out of total of 120
                letterSize = prop*(30/sum_for_prop) #Size parametre for all labels in the 3d plot
                letterDis = prop*(30/sum_for_prop) #Distance parametre of the labels and their ticks
                quality = prop*(20/sum_for_prop) #The higher the value the higher the quality of teh 3d plot
                max_2d_plane = 420 #Maximum coordinate for the x and y axis 
                                    #(extra above 400 is for projection of 3d graph onto z plane)
                
                z_upperlim = get_z_axis_max(Z)
                
                if typ == 0: #HA data (Input by user was 1)
                
                    E_ang = 30 #Angle of elevation
                    colors = ['jet', 'RdGy_r', 'hot']
                    for i in colors:
                        
                        low_H_ang = 181
                        high_H_ang = 270
                    
                        if i == 'hot': #Produce images to create horizontal rotation GIF

                            for H_ang in range( low_H_ang , high_H_ang ,1): #Mid angle within this range is (226, 227, 1)
                                                           #Actual good visible range -> (181, 270,1)
                                
                                plt.figure(figsize = (quality,quality))
                                ax = plt.axes(projection= "3d")
                                
                                ax.set_title(names[typ], fontproperties = 'Times New Roman', size = letterSize+30, y = 1, pad = prop*(5/sum_for_prop))
                                ax.set_ylabel("y-axis pixels", size = letterSize, labelpad = letterDis)
                                ax.set_xlabel("x-axis pixels", size = letterSize, labelpad = letterDis)
                                ax.set_zlabel("Photpix", size = letterSize, labelpad = letterDis+5)
                                ax.minorticks_on()
                                
                                #Function that converts sizes of x, y and z ticks to custom size
                                tick_sizes(ax, letterSize/1.7)
                                
                                ax.plot_surface(X,Y,Z, cmap = i)
                                
                                ax.view_init(E_ang, H_ang) #(<elevated angle>, <horizontal angle>)
                                plt.show()
                        
                        elif i == "RdGy_r": #Produce images to create more complicated horizontal rotation GIF
                            
                            for H_ang in range(low_H_ang , high_H_ang, 1): #Mid angle within this range is (226, 227, 1)
                                                           #Actual good visible range -> (181, 270,1)
                                
                                plot_contour_3d_graph(names[typ], X,Y,Z, quality, color = i, 
                                                        x_range = [0,500], y_range= [0,500],
                                                        z_min = -100, l_Size = letterSize, 
                                                        l_Dis = letterDis, lvls = Levels, 
                                                        el_angle = E_ang, horz_angle = H_ang,
                                                        z_upperlim = z_upperlim,
                                                        vert_cbar_name= "Level Colorbar", used_in_Results = True,
                                                        Z = Z)
                                
                        elif i == "jet": #Only make one image file
                            H_ang = 226
                            plot_contour_3d_graph(names[typ], X,Y,Z, quality, color = i, 
                                                    x_range = [0,500], y_range= [0,500],
                                                    z_min = -100, l_Size = letterSize, 
                                                    l_Dis = letterDis, lvls = Levels, 
                                                    el_angle = E_ang, horz_angle = H_ang,
                                                    z_upperlim = z_upperlim,
                                                    vert_cbar_name= "Level Colorbar", used_in_Results = True,
                                                    Z = Z)
                            
                elif typ == 1: #OIII data (Input by user was 2)
                    # color = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
                    #fake2Dline = lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
                                
                    E_ang = 11
                    for H_ang in range(181,270,1):
                        color = 'nipy_spectral'
                        plot_3d_Dust(names[typ], X, Y, Z, quality, color = color, 
                                    x_range = [0,max_2d_plane], y_range = [0,max_2d_plane], 
                                    z_min = 0, l_Size = letterSize, 
                                    l_Dis = letterDis, el_angle = E_ang, 
                                    horz_angle = H_ang, lvls = Levels, z_upperlim = z_upperlim,
                                    vert_cbar_name= "Level Colorbar", used_in_Results = True)
                        
                elif typ == 2: #SII data (Input by user was 3)
                    #color = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
                    
                    #fake2Dline = lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')

                    color = 'gnuplot'
                    
                    z_upperlim = get_z_axis_max(Z)
                    z_lowerlim = get_z_axis_min(Z)
                    
                    E_ang = 11
                    for H_ang in range(181,270,1):
                        plot_3d_Dust(names[typ], X, Y, Z, quality, color, 
                                    x_range = [0,max_2d_plane], y_range = [0,max_2d_plane], 
                                    z_min = z_lowerlim, l_Size = letterSize, 
                                    l_Dis = letterDis, el_angle = E_ang, 
                                    horz_angle = H_ang, lvls = Levels, z_upperlim = z_upperlim,
                                    vert_cbar_name= "Level Colorbar", used_in_Results = True)

            else:
                corrector()
        elif typ == 3:
            
            HA, O_3, S_2 = KDE_3d_Contour_combined_query()
            
            arrs = filtered_arrs(multiple = True, HA = HA, O_3 = O_3, S_2 = S_2) 
            
            X, Y, Z_1, Z_2, Z_3 = get_coords(max_x = 400, max_y = 400, groupedIMGArray = arrs, arrayNum = typ, multiple = True )
            #arrayNum = 1 -> OIII data
            #arrayNum = 0 -> HA data
            #arrayNum = 2 -> SII data
                            #Scale is out of total of 120
            letterSize = prop*(30/sum_for_prop) #Size parametre for all labels in the 3d plot
            letterDis = prop*(30/sum_for_prop) #Distance parametre of the labels and their ticks
            quality = prop*(20/sum_for_prop) #The higher the value the higher the quality of teh 3d plot
            max_2d_plane = 420 #Maximum coordinate for the x and y axis 
                                #(extra above 400 is for projection of 3d graph onto z plane)
            
            z_upperlim = get_z_axis_max(Z_1 = Z_1, Z_2 = Z_2, Z_3 = Z_3)
            z_min = get_z_axis_min(Z_1 = Z_1, Z_2 = Z_2, Z_3 = Z_3)

            # color = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
            #fake2Dline = lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
            
            E_ang = 30
            counter = 15
            for H_ang in range(180+counter,270,1):
                print()
                print("""_________Graph %d_________""" % counter)
                print()
                plot_combined('Combination', X, Y, quality, color = 'jet_r', 
                            x_range = [0,max_2d_plane], y_range = [0,max_2d_plane], 
                            z_min = z_min , l_Size = letterSize, 
                            l_Dis = letterDis, el_angle = E_ang, 
                            horz_angle = H_ang, lvls = Levels, z_upperlim = z_upperlim,
                            vert_cbar_name= "Kernal Density Estimate", used_in_Results = True, 
                            Z_1 = Z_1, Z_2= Z_2, Z_3 = Z_3)
                counter += 1
            return  X, Y, Z_1, Z_2, Z_3
    else:
        corrector()
        
    plt.show() # Show all wanted plots at once

main(arrs)