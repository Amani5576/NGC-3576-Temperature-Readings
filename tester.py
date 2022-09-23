
lists = XYm_Lists

collage = int(input("""

Produce images of HA -> Type 0
Produce images of OIII -> Type 1
Produce images of SII -> Type 2
                    """))

for i in range(3):
    if collage == i:
        filt = [] #Creating list for storing filtered lists Data
        for x in range(len(lists)): #looping through length of array lists
            for num in range(Levels):
                d = num
                filt.append(levelFilter(lists[x]))
                data = filt[i]
                arr = np.zeros([400,400]) # Create a 400x400 matrix of zeros
                for coord in data:
                    arr[coord[1], coord[0]] = 1 # Adds filtered data to the 
                plt.xlabel("Image X-axis")
                plt.ylabel("Image Y-axis")
                plt.title("%s (lvl %d)" % (names[i],d))
                plt.axis('off')
                plt.imshow(arr, cmap=plt.cm.gray)
                plt.figure() # Show plot in its own windowclear