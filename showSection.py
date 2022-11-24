# Intensity Spectra of Nebulae
# S. Amani Njoroge
# 4060924
# ShowSection

from DataAnalysis import arrs #Importing arrays
from FitsExtraction import fitFiles
import matplotlib.pyplot as plt

colors = plt.cm.magma #Making Background black and data white.

def show(filename):
    
    for ind in range(3):
        if filename == fitFiles[ind]: #Checking whether input data is same as output
            N1 = plt.Normalize(arrs[ind].min(), arrs[ind].max())
            #Creation of a normalizer based on min value to max value
            """Normalizing colour band makes sure
            entire range of black to white is 
            used for particular data set""" 
            arrsNorm0 = colors(N1(arrs[ind])) #Normalizing the matrix values
            '''new matrix will have assigned colours for each pixel
               based on pixel value. The higher the value the brighter the grey 
               (towards white) and the lower the value the darker the grey (towards black)
            '''
            plt.axis("off") #No axis on the image
            plt.title(fitFiles[ind]) #Title of the image
            plt.imshow(arrsNorm0) #pyplot DAature tospit out the array in an image
    plt.show()