# Intensity Spectra of Nebulae
# Samwel Amani Njoroge
# 4060924

# Importing arrays from Amani's code (arrs -> images, levels -> user input, XYm_Lists -> filtered images)
from DataAnalysis import arrs, Levels, XYm_Lists, names, stDev_arr, min_vals, max_vals, corrector, median_arr, modes_arr, up_q_arr, low_q_arr
import matplotlib.pyplot as plt # Import matplotlib library for plotting
import matplotlib.colors as col # Import matplotlib library for color mapping
import numpy as np # Import numpy library for array arithmetic
import showSection as ss
from scipy.stats import norm #getting norm to gain probability density function
from tabulate import tabulate as tb
from scipy.optimize import curve_fit
from math import floor, log10

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
def rounder(val,unc):
    length = len(str(unc)) #getting length of uncertainty
    val = round(val,-(length-1))
    
    return val

def collager():
    
    if ViewChosen != "special":
        collage = "more"
    else:
        collage = input("""

Printing filtered image of each intenisty level seperately:
        
Produce images of HA -> Type 0
Produce images of OIII -> Type 1
Produce images of SII -> Type 2
    """)

    return collage

def gauss(x,A,mu,sig): #Creating Gaussian function
        a = A*np.exp(-(x-mu)**2/sig**2)
        return a
    
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
Sulphur 2? Type 2
    
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
    for i in ViewChosen: #Looping thorugh all choices
        if i not in ViewingChoices: #If the user input is invalid
            corrector()
            
elif ViewChosen[0] == "special":
    
    collage = collager()
    
    if collage not in ["0","1","2"]: #If collage choice is invalid
        corrector()
    elif collage in ["0","1","2"]: #If the
        for i in range(3): #Looping through length of choisen (in this case just 3)
            if int(collage) == i: #If interger collage chosen is equal to the current i value
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

collage = collager()

if collage == "more" or ViewChosen in ViewingChoices[:-1] :
                    #Or if the choices were more than just special
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
        flat.append(arrs[1].flatten())
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

    
    #______________________________________________________________________________________________

    if "G" in ViewChosen:
        plt.figure(7)
        hist2 = plt.hist(arrs[0].flatten(), bins = binRange,density = True, rwidth=0.5) #Creating histogram 2
        line2 = plt.plot(domain, norm.pdf(domain,np.mean(arrs[0]),stDev_arr[0]),label = "Estimate probability curve", c= "black")
        #Creating normalised version of graph
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
            
else:
    if ViewChosen not in ViewingChoices:
        corrector()
        
    #_______________________Counting pixels that are not 0_____________________________

    print("")
    print("_____Number of non-zero Pixels______")
    print("")
    notE = []
    for i in range(len(names)):
        counter = 0
        countArray = []
        for ox in arr[i]:
            counter = list(ox).count(0)
            countArray.append(counter)

        notempty = len(arr[i])**2 - sum(countArray)
        notE.append(notempty)
        print(names[i], " = ", notE[i])
    
    dust = arr[1]+arr[2]
    countArray = []
    for d in dust:
        counter = list(d).count(0)
        countArray.append(counter)
    notempty = len(arr[i])**2 - sum(countArray)
    print("")
    print("Number of Dust pixels = ", notempty)

plt.show() # Show all wanted plots at once