# Intensity Spectra of Nebulae
# S. Amani Njoroge
# 4060924
# ShowSection

from DataAnalysis import arrs #Importing arrays

import matplotlib.pyplot as plt

colors = plt.cm.gray #Making Background black and data white.

def show(filename):
    
    if filename.endswith(".fit") == True:
        if filename.startswith("OIII") or filename.startswith("SII") or filename.startswith("HA"):
            if filename == "HA.fit": #Checking whether input data is same as output
                N1 = plt.Normalize(arrs[0].min(), arrs[0].max())
                #Creation of a normalizer based on min value to max value
                """Normalizing colour band makes sure
                entire range of black to white is 
                used for particular data set""" 
                arrsNorm0 = colors(N1(arrs[0])) #Normalizing the matrix values
                '''new matrix will have assigned colours for each pixel
                   based on pixel value. The higher the value the brighter the grey 
                   (towards white) and the lower the value the darker the grey (towards black)
                '''
                
                plt.axis("off") #No axis on the image
                plt.title("Hydrogen Alpha") #Title of the image
                plt.imshow(arrsNorm0) #pyplot DAature tospit out the array in an image
                
            elif filename == "OIII.fit":
                N2 = plt.Normalize(arrs[1].min(), arrs[1].max())
                arrsNorm1 = colors(N2(arrs[1]))
                plt.axis("off")
                plt.title("Oxygen III")
                plt.imshow(arrsNorm1)
                
            elif filename == "SII.fit":
                N3 = plt.Normalize(arrs[2].min(), arrs[2].max())
                arrsNorm2 = colors(N3(arrs[2]))
                plt.axis("off")
                plt.title("Silicon II")
                plt.imshow(arrsNorm2)
        else: 
            print("You typed the name of file wrongly: HA, OIII and SII are the only existing ones")
    else:
        print("You have not inserted the name properly: <name.fit>")
    plt.show()