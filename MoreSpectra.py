# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:50:06 2022

@author: Amani
"""
from spectra import SeeDats
from DataAnalysis import stDev_arr, min_vals, max_vals, arrs, plot_Titles # Importing arrays from Amani's code (arrs -> images, levels -> user input, XYm_Lists -> filtered images)
import matplotlib.pyplot as plt # Import matplotlib library for plotting
from scipy.stats import norm
import numpy as np # Import numpy library for array arithmetic

#Plotting the Quartile Data__________________________
# flat = []
# for file in arrs:
#     flat.append(file.flatten())
    
# plt.ylabel("Photpix", size = 14)
# plt.boxplot(flat,labels=plot_Titles)
# plt.show()
# plt.clf()
#____________________________________________________


if SeeDats == "G" or SeeDats == "B":
    plt.show()