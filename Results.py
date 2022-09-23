# Intensity Spectra of Nebulae
# Samwel Amani Njoroge
# 4060924

# Importing arrays from Amani's code (arrs -> images, levels -> user input, XYm_Lists -> filtered images)
from DataAnalysis import arrs, Levels, XYm_Lists, names, stDev_arr, min_vals, max_vals, corrector
import matplotlib.pyplot as plt # Import matplotlib library for plotting
import numpy as np # Import numpy library for array arithmetic
import showSection as ss
from scipy.stats import norm #getting norm to gain probability density function
from tabulate import tabulate as tb

#Tuple-filtering function
def levelFilter(tuplist): 
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
    return templist

#Funtion that enables user to skip through unneccesary heavy printing such as tuples.

showUnfilt = input("""
Would you first like to see what the Nebula looks like before filtering out the data?

Y/N?

      """)
      
if showUnfilt == "Y":
    unfiltImg = input("""
Which one would you like to see?
    
Hydrogen Alpha? Type 0
Oxygen 3? Type 1
Silicon 2? Type 2
    
All the above? type all

          """)
          
    if unfiltImg == "0":
        ss.show("HA.fit")
    elif unfiltImg == "1":
        ss.show("OIII.fit")
    elif unfiltImg == "2":
        ss.show("SII.fit")
    elif unfiltImg == "all":
        ss.show("HA.fit")
        ss.show("OIII.fit")
        ss.show("SII.fit")
    else:
        corrector()
        
elif showUnfilt == "N":
    pass
else: 
    corrector()

def viewing(): 
    
    x = input("""
                       
Desired output:
    
*Tuples of coorindate data?  -> T
(Printing Tuples might take some time)

*Graphs and Pie Charts -> Then type G

*Tables -> TB

*Images -> I

*A Combination. E.g Graphs and Pie Charts, Images and Tuples-> G,I,T

*All the above? -> Then Type the Letter A

*SPECIAL CHOICE: -> Type the word: special

""")
    print("---------------------------------------------------------")
    print("")
    
    #Convert choice string input into list of those characters
    x = x.split(",") #Automatically splits every string element based on the specified arguement splitter
    #Overwriting "x" with its new list form rather than remianing as string.
    return x

ViewingChoices = ["T","G","TB","I","A","special"]


ViewChosen = viewing() #Storing the type of data user wants to see in variable

if type(ViewChosen) == list and ViewChosen[0] != "special":
    for i in ViewChosen:
        if i not in ViewingChoices:
            corrector()
            
elif ViewChosen[0] == "special":
    
    collage = input("""

Printing filtered image of each intenisty level seperately:
    
Produce images of HA -> Type 0
Produce images of OIII -> Type 1
Produce images of SII -> Type 2

choose more definitive printing? type the word: more

""")

    if collage in ["0","1","2"]:
        for i in range(3):
            if int(collage) == i:
                filt = [] #Creating list for storing filtered lists Data
                for num in range(Levels+1):
                    d = num
                    filt = levelFilter(XYm_Lists[i])
                    arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
                    for coord in filt:
                        arr[coord[1], coord[0]] = 1 # Adds filtered data to the 
                    plt.xlabel("Image X-axis")
                    plt.ylabel("Image Y-axis")
                    plt.title("%s (lvl %d)" % (names[i],d))
                    plt.axis('off')
                    plt.imshow(arr, cmap=plt.cm.gray)
                    plt.figure() # Show plot in its own windowclear
                    plt.show()
                    
    elif collage == "more":
        filt = [] #Creating list for storing filtered XYm_Lists Data

        #Note that input() automatically converts user intput into a string
        if Levels !=1: #If there is more than just one level
            choice = input("""
                                       
        Would you like to see all levels from highest to chosen level ? If so type "Yes" or "all"
        (make sure to use quotation marks)

        Or 

        Would you like to see only one level ? If so type the integer level number:
            
        Or

        Would you rather specific levels (more than one)? 
            e.g: Only want pixel coordinate with the highest value: type -> 0
                 Only level 2 and level 3: then type -> 2,3
                 Only Level 6 and level 31 and level 4: then type -> 6, 31 , 4
                 (spacing doesnt matter, but make sure to separate using commas)
                 A range from 4 to 50: then type -> 4:50
                         
                            """)
            print("---------------------------------------------------------")
            print("")
            
            #NOTE: 'choice' variable is only a string list and needs to be converted for proper usage:

            numbers = ["1","2","3","4","5","6","7","8","9"]
            if "," in choice: #If multitude of specific levels are chosen
                #Convert choice string input into list of those specific levels
                f = choice.split(",") #Automatically splits every string element based on the specified arguement splitter
                #f is an array of strings with each string being a level number
                d = [] #Element to store integer values
                for i in f: #for every string element
                    d.append(int(i)) #adding integer version of each number string into new list
            elif "," not in choice and choice[0] in numbers and ":" not in choice: #if the input was only of one level
                d = int(choice) #Convert level from string to integer
            elif ":" in choice: 
                d = [] #Element to store integer values
                ind = choice.index(":")
                for i in range(int(choice[:ind]),int(choice[ind+1:])+1): #starting from n ending at m where [n:m] where "m' is included
                    d.append(i)
            else: 
                d = choice #Remains as string
                
            #________________________________________________________________________________________________________________________________________
            
            for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
                #function that filters lists by removing unwanted tuples based on chosen level from user input
                filt.append(levelFilter(XYm_Lists[x])) #levelFilter returns a filtered out (or shortened) list of tuples
            #________________________________________________________________________________________________________________________________________
            
            
            #Printing of Tuple Data of coordinates when Levels constructed are more than one
            if ViewChosen == "T" or ViewChosen == "A": 

                print("NOTE: data output will be given as: ( <x-coord> , <y-coord> , <Intensity level> )")
                print("")
                print("If <Intensity level> = 0, then this is the only pixel in the matrix that has the largest number of photons")
                print("")
                
                for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
                    
                    #If the current data is of empty list
                    if XYm_Lists[x] == []:
                        print("Coordinates of %s from intensity Level 1 -> %d:" % (names[x],Levels))
                        print("")
                        print("There are no intenisties within Level 1 -> %d for %s" %(Levels, names[x]))
                        print("")
                        
                    #if the input is "yes" or "all"
                    if type(d) == str:#Making sure its not case sensitive by just checking if its a string
                        print("Coordinates of %s from intensity Level 1 -> %d:" % (names[x],Levels))
                        print("")
                        print(XYm_Lists[x]) #Print the list of tuples
                        print("")
                    
                    else: #If user input was a specific level or a multitude of levels
                        print("Coordinates of %s in levels %s data:" % (names[x],choice))
                        print("")
                        print(filt) #printing out filtered tuples
                        print("")

        #Printing of Tuple Data of coordinates with no constructed levels. (Only just Level 1)               
        else: 
            if ViewChosen == "T" or ViewChosen == "A": #If user want to see tuple data
                for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
                    print("Coordinates of %s from intensity Level 1:" % (names[x]))
                    print("")
                    print(XYm_Lists[x]) #Print the list of tuples
                    print("")

        def plot_spectrum(x): # Create a function to plot the spectrum
            pixels = np.mean(x, axis=1) # Get average of all pixels relative to x-axis
            # Plot the resultant spectrum
            plt.plot(range(len(pixels)), pixels)
            plt.xlabel("Pixel Number (relative to x-axis)")
            plt.ylabel("Light Intensity relative to x-axis (Arbitrary Unit)")

        # for file in arrs:
        #     plot_spectrum(file)
        # plt.title(f"Intensity Spectrum of Nebulae") # Title of the plot for all nebulae
        # plt.legend(names) # Legend of the plot
        # plt.figure() # Show plot in its own window


        #______________UQ, Median and LQ Data___________________
        if "G" in ViewChosen:
            flat = [] #Stores 2D data of HA file into 1D
            for i, file in enumerate(arrs):
                flat.append(file.flatten())
                
            plt.ylabel("Photpix")
            plt.boxplot(flat, labels = names)
            plt.figure()

        #____________________Filtered Images__________________________________________________________________
        for i,data in enumerate(filt):
            arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
            
            for coord in data: # Loops through each of the filtered data, plots accordingly
                arr[coord[1], coord[0]] = 1 # creating the filtered version of the original matrix
                # (Max = Levels - 0, where 0 -> Max intensity)
            
            if "I" in ViewChosen: #If user asked for Image Display of new filtered matrix
                plt.imshow(arr, cmap=plt.cm.gray)
                plt.xlabel("Image X-axis")
                plt.ylabel("Image Y-axis")
                plt.title("%s" % names[i])
                plt.axis('off')
                plt.figure() # Show plot in its own window
                plt.show()

                # plot_spectrum(arr.transpose())
                # plt.title(f"Filtered spectrum data for {names[i]}")
                # plt.figure() # Show plot in its own window
                
        domain = range(min_vals[0],max_vals[0],1) #Domain is from minimum to maximum of  Photpix of HA
        step = 5
        binRange = np.arange(domain[0], domain[-1], step) #binwidth of histograms

        #__________Histograms_________________________________________________________________________
        plt.figure(1) #Figure 1 is for 1st histogram
        hist1 = plt.hist(arrs[0].flatten(), bins = binRange, density = False, rwidth=0.5) #Creating histogram 1
        plt.xlabel("Photpix", size = 13)
        plt.ylabel("Number of Pixels", size = 13)

        plt.figure(2)
        hist2 = plt.hist(arrs[0].flatten(), bins = binRange,density = True, rwidth=0.5) #Creating histogram 2
        #______________________________________________________________________________________________

        if "G" in ViewChosen:
            line1 = plt.plot(hist2[1][0:-1]+(step/2),hist2[0], label= "Normalised curve of trend", c = "red") #Creating line trend for 
            #Adding +2.5 to each x-data point allows the line trned to touch center of top of bar
            line2 = plt.plot(domain, norm.pdf(domain,np.mean(arrs[0]),stDev_arr[0]),label = "Estimate probability curve", c= "black")
            #Creating normalised version of graph
            plt.ylabel("Normalised Number of Pixels", size = 13)
            plt.xlabel("Photpix", size = 13)
            plt.legend()
            plt.figure()
        else: #Do not show histograms
            plt.close(1)
            plt.close(2)

        #_________Table 1_____________

        tempHist = hist1[1]+round((step/2),1) #Making the x-axis centered
        tempHist = tempHist.round() #Rounding off due to photons concpetually being a whole rather than a fraction

        #Finding the Average maximum Photpix.
        h1_l = list(hist1[0]) #Converting to ordinary list to use max()
        max_h1 = hist1[0].max() #Getting maximum number of pixels (The group from the histogram)
        index  = h1_l.index(max_h1) #Getting index number of that maxium group within histogram data
        Photpix_max_av = list(tempHist)[index] #getting the max average Photpix

        # #Shortnening the table`
        # zipped = list(zipped)
        # for ind,x in enumerate(zipped):
        #     if ind%2 != 0: #If the index number is odd
        #         zipped.pop(ind)

        #Use of Wien's displacement law
        b = 2897771.955 #Wien's displacement constant in nm Kelvins
        lmbd = 656.281 #wavelength of H_A emission line in nm
        Temp = b/lmbd  #Temperature in Kelvin
        ratio = Temp/Photpix_max_av #Ratio between maximum average Photopix (from histogram) and Temperature of HA wavelength (from Weins law).
        Temps = [] #Stores all corresponding temperatures based on the ratio of highest peak to the Temp.

        for x in tempHist: #Converting average bin of histogram photopix to temperature.
            Temps.append(round(ratio*x,3))

        titles = ["Photpix","Number of Pixels","Temperature (K)"] #Headers for table
        zipped = zip(tempHist,hist1[0],Temps) #Zipping up each coordiate into tuples
        Zip = list(zipped) #Used in creation of smaller tables
        table = tb(Zip,headers = titles, tablefmt = "fancy_grid") #creating table 
        if "TB" in ViewChosen or "A" in ViewChosen:
            print(table)

        #_________Pie Chart 1 (On All Temperatures)_____________

        if "G" in ViewChosen:
            exploders = [] #Stroing exploders for pie chart.
            for x in hist1[0]: #Looping through number of Pixels within table 1
             #Aids in making the pie chart a bit more readerable
                if x > 10000:
                    exploder = 0
                elif x > 1000:
                    exploder = 1
                elif x > 100:
                    exploder = 2.8
                else: 
                    exploder = 4
                exploders.append(exploder) #adding exploder values into exploders list
            plt.title("Distribution of All Temperatures in NGC 3576")
            plt.pie(hist2[0], labels = Temps[0:-1], explode = exploders)
            plt.figure()
            
        #_________Segregation of temperatures_____________

        #Based on thier magnitude
        mag_Temps = [[],[],[],[]]
        #Getting splitting constant for segregation
        seg_cons = (max(Temps) - min(Temps))/4

        for ind,x in enumerate(mag_Temps):
            for y in Temps:#Looping through each Temperature value.
                if (max(Temps) - seg_cons*(ind)) >= y > (max(Temps) - seg_cons*(ind+1)):
                    x.append(y)

        #__________Segregation of zipped tuples_________________________

        #Based on magnitude of Temperatuers
        seg_zips = [[],[],[],[]]

        for x in Zip:
            for j,y in enumerate(mag_Temps):
                for y1 in y:
                    if x[2] == y1:
                        seg_zips[j].append(x)

        #_________Smaller(Temp-segragated) Tables_____________

        for i in seg_zips:
            table1 = tb(i,headers = titles, tablefmt = "fancy_grid") #creating table 
            if "TB" in ViewChosen or "A" in ViewChosen:
                print(table1)
            
        #________________Other Pie Charts_________________

        if "G" in ViewChosen:
            LtoS = ["Largest","Large","Median","Smallest"]

            for x in range(len(seg_zips)): #Looping through number of elements in seg_zips
                
                # *a makes the array "a" appear wihtout its outer brackets.
                newList = list(zip(*seg_zips[x])) #Unzipping
                
                plt.title("Distribution of %s Temperatures (in K)" % LtoS[x])
                plt.pie(newList[1], labels = newList[2])
                #newList[2] = Relative Temperatures
                #newList[1] = Relative Number of Pixels
                plt.figure()
else:
    if ViewChosen not in ViewingChoices:
        corrector()
        
plt.show() # Show all wanted plots at once