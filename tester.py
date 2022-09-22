# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:33:19 2022

@author: Amani
"""

for num in range(1,15):
    filt = [] #Creating list for storing filtered XYm_Lists Data
    d = num

    for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
        filt.append(levelFilter(XYm_Lists[x]))
        for i, data in enumerate(filt):
            arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
            for coord in data:
                arr[coord[1], coord[0]] = 1 # Adds filtered data to the 
            plt.xlabel("Image X-axis")
            plt.ylabel("Image Y-axis")
            plt.title("%s (lvl %d)" % (names[ind],d))
            plt.axis('off')
            plt.imshow(arr, cmap=plt.cm.gray)
            plt.figure() # Show plot in its own window

#___________For HA_____________________________

for num in range(100):
    filt = [] #Creating list for storing filtered XYm_Lists Data
    d = num

    for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
        filt.append(levelFilter(XYm_Lists[x]))
        
    data = filt[0]
    arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
    for coord in data:
        arr[coord[1], coord[0]] = 1 # Adds filtered data to the 
    plt.xlabel("Image X-axis")
    plt.ylabel("Image Y-axis")
    plt.title("%s (lvl %d)" % (names[0],d))
    plt.axis('off')
    plt.imshow(arr, cmap=plt.cm.gray)
    plt.figure() # Show plot in its own windowclear
    
#__________For OIII____________________________

for num in range(100):
    filt = [] #Creating list for storing filtered XYm_Lists Data
    d = num

    for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
        filt.append(levelFilter(XYm_Lists[x]))
        
    data = filt[1]
    arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
    for coord in data:
        arr[coord[1], coord[0]] = 1 # Adds filtered data to the 
    plt.xlabel("Image X-axis")
    plt.ylabel("Image Y-axis")
    plt.title("%s (lvl %d)" % (names[1],d))
    plt.axis('off')
    plt.imshow(arr, cmap=plt.cm.gray)
    plt.figure() # Show plot in its own windowclear
    
#__________For SII____________________________

for num in range(100):
    filt = [] #Creating list for storing filtered XYm_Lists Data
    d = num

    for x in range(len(XYm_Lists)): #looping through length of array XYm_Lists
        filt.append(levelFilter(XYm_Lists[x]))
        
    data = filt[2]
    arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
    for coord in data:
        arr[coord[1], coord[0]] = 1 # Adds filtered data to the 
    plt.xlabel("Image X-axis")
    plt.ylabel("Image Y-axis")
    plt.title("%s (lvl %d)" % (names[2],d))
    plt.axis('off')
    plt.imshow(arr, cmap=plt.cm.gray)
    plt.figure() # Show plot in its own windowclear
