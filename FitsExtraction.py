# Intensity Spectra of Nebulae
# S. Amani Njoroge
# 4060924
# FitsExtraction

from astropy.io import fits
import numpy as np

fitFiles = ["HA.fit", "OIII.fit", "SII.fit"]

#Dictionary for usage in getting the numpy data and its type
numpyDatTyp = { 8: "numpy.uint8 (note it is UNsigned integer)",
               16: "numpy.int16",
               32: "numpy.int32",
               64: "numpy.int64",
              -32: "numpy.float32",
              -64: "numpy.float64"
              }

print("_________________HDULists________________________")
#Below returns a HDUList of the Fit data files.

HDUs = [] #List to store HDU (Header Data Unit) for HA, OIII and SII.

for x in range(len(fitFiles)):#looping through length of array
    HDUs.append(fits.open(fitFiles[x])) #Open fits file and add HDU data into HUDs array
    print(HDUs[x].info()) #Outputs a Summary of the info of the HDU List.
    print("")

print("_______Impotant Header information from all PrimaryHDU's_______")
print("")

#Getting key names from ver long Primary HDU Dictionary
head0 = fits.getheader(fitFiles[x]) # Could have used (h) or (i) but all info are equivalent
#This is only useful for looking at the key names within the Primary HDU's.
"""
print(head0) is astropy's version of head0.keys() to get key names.
In addition, this printing method also shows the assigned data to each key.
"""

#Using getval() to get specific information from Primary and Image HDU

print("Name of Object: ", fits.getval(fitFiles[x],"OBJECT"))
print("Number of data Axes for ImageHDU: ", fits.getval(fitFiles[x],"NAXIS1"), "pixels")
print("Resolution: ", fits.getval(fitFiles[x],"RESOLUTN")," ", fits.getval(fitFiles[x],"RESOUNIT"))
print("Color Spacing: ", fits.getval(fitFiles[x],"COLORSPC"))
print("Approximate right ascension in hours: (", fits.getval(fitFiles[x],"OBJCTRA"), ")")
print("Approximate declination: (", fits.getval(fitFiles[x],"OBJCTDEC"), ") degrees")

BITPIXData = fits.getval(fitFiles[x],"BITPIX") #Getting BitPixelData from Primary HDU
if BITPIXData in numpyDatTyp: #If the bitPixel number is in the defined dictionary
    print("number of bits per data pixel: ", BITPIXData, " meaning of type ", numpyDatTyp[BITPIXData])
print("")

HDUDataTitles = ["__________________HA ImageHDU Data_________________________","__________________OIII ImageHDU Data_________________________", "__________________SII ImageHDU Data_________________________"]

#Displaying the default data Matrix from PrimaryHDU's of HA, OIII and SII
for x in range(len(fitFiles)): #Looping through length of array fitFiles
    print(HDUDataTitles[x]) #Print the relative title
    print("")
    print(HDUs[x][1].data) #From the image HDU, show the ImageHDU of current fitFile.
    print("")

tempArray = np.array(HDUs[0][1].data) #converting image HDU file into a numpy matrix
pixelNum= np.shape(tempArray)[0] #Getting the row number of matrix