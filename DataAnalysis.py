# Intensity Spectra of Nebulae
# S. Amani Njoroge
# 4060924
# DataAnalysis

from FitsExtraction import HDUs, agree, disagree, corrector #importing HDU Data Sets from FIT files as well as copies of the Fit files
import numpy as np #Importing numpy for useful array manipulation.
from statistics import median, multimode, stdev
import matplotlib.pyplot as plt
import matplotlib.colors, matplotlib.cm, matplotlib.markers
import csv, sys, itertools, threading, time
import scipy

#animation for processing request of task ('loading')
def animate():
    for c in itertools.cycle(['.', '..', '...', '....', '    ']):
        if processing:
            sys.stdout.write('\rProcessing ' + c)
            sys.stdout.flush()
            time.sleep(0.3)
        else:
            break
    sys.stdout.write('\rDone!     ')

#Returns lowest Z-value(s)
def get_z_axis_min(**kwargs):
    
    def mini_get_z_axis_min(Z):
        
        arr = np.array(Z).flatten() #Flattening the matrix to array of size 1
        u, c = np.unique(arr, return_counts=True)
        # u -> Unique pixel values (already sorted in ascending order)
        # c -> Number of occurences of those pixel values
        
        if min(u) == -1:
            try:
                min_val = u[1] #Return the next smallest unique value
            except IndexError: #If only filled with -1's 
                return 0 #Set minimum to 0
        else:
            min_val = u[0]
        
        return min_val
    
    if 'Z' in kwargs:
        minimum_z = mini_get_z_axis_min(kwargs['Z'])
    
    else:#If multiple Z's are involved
        p_s = [] #Storing all the min values from matrices: Z_1, Z_2, Z_3
        for k,v in kwargs.items():
            p = mini_get_z_axis_min(v)
            p_s.append(p)
        
        #Get major maximum from all graphs
        minimum_z = min(p_s) 
        
    return minimum_z

#Returns highest Z-value(s)
def get_z_axis_max(**kwargs):
    
    def mini_get_z_axis_max(Z):
        
        arr = np.array(Z).flatten() #Flattening the matrix to array of size 1
        u, c = np.unique(arr, return_counts=True)
        # u -> Unique pixel values (already sorted in ascending order)
        # c -> Number of occurences of those pixel values
                
        return max(u)
    
    if 'Z' in kwargs:
        maximum_z = mini_get_z_axis_max(kwargs['Z'])
    
    else:#If multiple Z's are involved
        p_s = [] #Storing all the max values from matrices: Z_1, Z_2, Z_3
        for k,v in kwargs.items():
            p = mini_get_z_axis_max(v)
            p_s.append(p)
        
        #Get major maximum from all graphs
        maximum_z = max(p_s) 
        
    return maximum_z

#converts sizes of x, y and z ticks to custom size
def tick_sizes(ax, size): 
    for t in ax.xaxis.get_major_ticks(): t.label.set_fontsize(size)
    for u in ax.yaxis.get_major_ticks(): u.label.set_fontsize(size)
    for v in ax.zaxis.get_major_ticks(): v.label.set_fontsize(size)

#Function gets proper coordinate structure for plotting into 3d
def get_coords(max_x, max_y, groupedIMGArray, arrayNum, multiple):
    
    if multiple == True:
        #Creating mimic of 400*400 pixel image  axis for y and x
        x = np.arange(0, 400, 1)
        y = np.arange(0, 400, 1)
        
        #Create mesh data
        X, Y = np.meshgrid(x, y)
        
        #Z axis is based on the input x and y coords into the image files
        Z_1 = groupedIMGArray[0][x][y]
        Z_2 = groupedIMGArray[1][x][y]
        Z_3 = groupedIMGArray[2][x][y]
    
        return (X, Y, Z_1, Z_2, Z_3)
    
    else:
        #Creating mimic of 400*400 pixel image  axis for y and x
        x = np.arange(0, 400, 1)
        y = np.arange(0, 400, 1)
        
        #Create mesh data
        X, Y = np.meshgrid(x, y)
        
        #Z axis is based on the input x and y coords into the image files
        Z = groupedIMGArray[arrayNum][x][y]
    
        return (X, Y, Z)

def blackTheme(fig, ax):
    fig.set_facecolor('black') #Black (for the figure itself)
    ax.set_facecolor('black') #Black (for axis area)
    
    #Converting each visible plane of the graph to be black
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    
    #Turning all tick labels (and ticks themselves) white
    [t.set_color('white') for t in ax.xaxis.get_ticklines()]
    [t.set_color('white') for t in ax.xaxis.get_ticklabels()]
    [t.set_color('white') for t in ax.yaxis.get_ticklines()]
    [t.set_color('white') for t in ax.yaxis.get_ticklabels()]
    [t.set_color('white') for t in ax.zaxis.get_ticklines()]
    [t.set_color('white') for t in ax.zaxis.get_ticklabels()]

def color_cmaps(color):
    col = ['jet', 'jet_r', 'RdGy', 'RdGy_r', 
           'hot', 'hot_r', 'Blues_r', 'Greens_r', 'Purples_r',
           'Blues', 'Greens', 'Purples']
    cm_s = [matplotlib.cm.jet, matplotlib.cm.jet_r, matplotlib.cm.RdGy, 
            matplotlib.cm.RdGy_r, matplotlib.cm.hot, matplotlib.cm.hot_r,
            matplotlib.cm.Blues_r, matplotlib.cm.Greens_r, matplotlib.cm.Purples_r,
            matplotlib.cm.Blues, matplotlib.cm.Greens, matplotlib.cm.Purples]
    
    for ind, c in enumerate(col):
        if color == c:
            return cm_s[ind] #returning color in form of matplotlib.cm.<color>
   
    #If there is no color in c
    sys.exit("color_maps function doesnt have '%s' in the lsit of its colors" % color)

def get_scaling_Factor():
    # Limitation based on Colour of an object in digital systems
    maxColor = 2**8-1 #0 -> 255

    #Creating user-input based Scale-Levels for relative intensity
    scF = int(input("""
                               
    Please input the number of levels.
                
    Its advisable to choose a high number such as %d or higher.
    Highest value to be chosen is %d due to a limitation of 
    Colour of an object in digital systems.

         
    """ % (int(maxColor/4),maxColor)))
    
    if scF > maxColor: #If scaling Factor is larger than 255 (pixel range limitation):
        print("""
              You have split the data into %d levels but the limitation (based on 2D pixel data) is %d in length/width. 
              """ % (scF, maxColor))

        scF = get_scaling_Factor()
  
    return scF

def get_levels(scF):
    l = int(input("""
    Levels have been successfully constructed. 

    Note: Highest intensity level = 1
          Lowest intensity level = %d
                                      
    Are you sure you want all the data to be processed and inputted till level %d?
    If so, then type %d again. 
            
    Input the number of level intensities you desire.
    (e.g. if you type 6, data will process from level 1 to 6)
    Recommended to choose upto the top quarter tier level such as level %d or lower. .
    (Warning: can take longer depending on processessing power of your device)     

    """ % (scF,scF,scF,int(scF/4))))

    print("_______________________________________________________________________________________________")
    print()
    
    if l > scF: #If the chosen number of levels are bigger than the Scaling Factor:
        print("""You have split the data into %d levels but have chosen your levels of interests to level %d. 
              """ % (scF, l))

        sys.exit("Please rerun the code and choose wisely.") #exiting the code with a message if the preceeding if statement is met
             
    return l

def fundamental_filt(XYm_Lists, arrs, max_vals, scales):
    #Commence fundamental filtration based on user scaling Factor and Levels
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
        
#Function sets contours and their colorbars
def set_contours(color, fig, l_Size, ax, option, data_Arr, min_Arr, max_Arr, cbarOutlinecol, **kwargs):
    axis = ['x','y','z']
    
    for i in range(option):
        
        if 'used_in_Results' in kwargs: #if specific key exists
            norm = matplotlib.colors.Normalize(vmin = 0, vmax = Levels) # Normalizing colors to user specified level E.g. From 0 to Level 100
            cmap = color_cmaps(color)
            cmap.set_under((0.1,0.1,0.1), alpha=0.2) #Converting all data (beneath Z = 0) transparent
                          # R,B,G   transparency
            
        if 'Z' in kwargs: #if only one Z matrix
            #Creating contours for z, x and y plane. (A superposition of sorts)
            cset = ax.contourf(data_Arr[0], data_Arr[1], kwargs['Z'], zdir = axis[i], offset = max_Arr[i], norm = norm, cmap = cmap)
          
            #Settings for Horizontal ColorBar
            prop_1 = 1 #Constant of proportional for size of colorbar
            
            if i == 0:
                
                cbar = fig.colorbar(cset, ax = ax, shrink = (0.5/prop_1), aspect = (20*prop_1), orientation = 'horizontal', pad = -prop*(0.05/sum_for_prop))
                
                #color bar tick labels are 3 times less than graph axis labels
                cbar.ax.tick_params(labelsize=l_Size/2, colors = cbarOutlinecol) 
                cbar.set_label("X and Y (independently) projected on the Z plane" , labelpad = prop*(15/sum_for_prop), size = prop*(20/sum_for_prop) , color = cbarOutlinecol, loc = 'center')
                cbar.ax.yaxis.set_tick_params(color = cbarOutlinecol, size = prop*(20/sum_for_prop))
                cbar.outline.set_edgecolor(cbarOutlinecol)
                
                #Setting axis limits to 3d graph
                ax.set_xlim(min_Arr[0], max_Arr[0])
            
            #Setting axis limits to 3d graph
            if i == 1:
                ax.set_ylim(min_Arr[1], max_Arr[1])
           
            if i == 2:  #max_Arr[2] contains minmum value of z
                        #min_Arr[2] contains maximum value of z
                ax.set_zlim(max_Arr[2], min_Arr[2])
            
    if 'Z_1' in kwargs: #If there are multiple Z-axes
    #Creating contours for z, x and y plane. (A superposition of sorts)

        zod, n = kwargs['zod'], kwargs['n']
        density, z_min_contour = kwargs['density'], kwargs['z_min_contour']

        a = 0.8 #contour transparency constant 0-> invisible, 1-> opaque
        
        # plot projection of density onto z-axis
        plotdat = np.sum(density, axis=2) 
        plotdat = plotdat / (np.max(plotdat))
        plotx, ploty = np.mgrid[0:400:100j, 0:400:100j]
        cset_1 = plt.contourf(plotx, ploty, plotdat, offset = z_min_contour, 
                              zdir='z', levels = n, cmap = color_cmaps(color), 
                              zorder = zod[0], alpha = a)
        
        #plot projection of density onto y-axis
        plotdat = np.sum(density, axis=1) #summing up density along y-axis
        plotdat = plotdat / np.max(plotdat)
        plotx, plotz = np.mgrid[0:400:100j, max_Arr[2]:min_Arr[2]:100j]
        cset_2 = plt.contourf(plotx, plotdat, plotz, offset=500, zdir='y', 
                              levels = n, cmap = color_cmaps(color), 
                              zorder = zod[0], alpha = a)
        
        #plot projection of density onto x-axis
        plotdat = np.sum(density, axis=0) #summing up density along z-axis
        plotdat = plotdat / np.max(plotdat)
        ploty, plotz = np.mgrid[0:400:100j, max_Arr[2]:min_Arr[2]:100j]
        cset_3 = plt.contourf(plotdat, ploty, plotz, offset=500, zdir='x', 
                              levels = n, cmap = color_cmaps(color), 
                              zorder = zod[0], alpha = a)
        
        return cset_1, cset_2, cset_3
    
def plot_contour_3d_graph(name, X, Y, quality, color, x_range, y_range, z_min, l_Size, l_Dis, el_angle, horz_angle, lvls, z_upperlim, vert_cbar_name, **kwargs):
  #(<Names of graph>, <x-list>, <y-list>, <z-lists>, < graph quality>, <colorscheme>, <Horizontal angle>, <levels based on grouping by user input prefernces e.g. 100 levels>)
    
    for k,v in kwargs.items():
        if k == 'Z':
            Z = v
    
    fig = plt.figure(figsize = (quality,quality))
    ax = plt.axes(projection= "3d")
    
    ax.set_title(name, fontproperties = 'Times New Roman', size = l_Size+30, y = 1, pad = prop*(5/sum_for_prop))
    ax.set_ylabel("y-axis pixels", size = l_Size, labelpad = l_Dis)
                                                        #distance between label and graph
    ax.set_xlabel("x-axis pixels", size = l_Size, labelpad = l_Dis)
    
    if 'used_in_Results' in kwargs: #if specific key exists
        ax.set_zlabel("Levels", size = l_Size, labelpad = l_Dis+5)
    else:
        ax.set_zlabel("Photpix", size = l_Size, labelpad = l_Dis+5)
        
    ax.set_zlim(z_min,z_upperlim)
    ax.minorticks_on()
    
    if 'used_in_Results' in kwargs: #if specific key exists
        set_contours(color, fig = fig, cbarOutlinecol = 'black', l_Size = l_Size, ax = ax, option = 3, data_Arr = [X,Y], min_Arr = [x_range[0],y_range[0],lvls], max_Arr = [x_range[1],y_range[1],z_min], used_in_Results = True, Z = Z)
    else:
        set_contours(color, fig = fig, cbarOutlinecol = 'black', l_Size = l_Size, ax = ax, option = 3, data_Arr = [X,Y], min_Arr = [x_range[0],y_range[0],lvls], max_Arr = [x_range[1],y_range[1],z_min], Z = Z)
    
    #Function that converts sizes of x, y and z ticks to custom size
    tick_sizes(ax, l_Size/2)
    
    # Creating plot
    if 'used_in_Results' in kwargs: #if specific key exists
        norm = matplotlib.colors.Normalize(0,Levels) # Normalizing colors to user specified level E.g. From 0 to Level 100
        cmap = color_cmaps(color)
        cmap.set_under((.5,.5,.5), alpha=0.3) #Converting all data (beneath Z = 0) transparent
        surf = ax.plot_surface(X,Y,Z, rstride = 1, cstride =1, norm = norm, cmap = cmap)
    else:
        surf = ax.plot_surface(X,Y,Z, rstride = 1, cstride =1, cmap = color)
    #cstride -> Striding long the each row since its equated to 1
    #if it was equal to 9, then its would skip 9
    #cstride -> Striding` long the each column since its equated to 1
    
    cbar = fig.colorbar(surf, ax = ax, shrink = 0.5, aspect = 10)
    cbar.ax.tick_params(labelsize=l_Size/2)
    cbar.set_label(vert_cbar_name , labelpad = prop*(25/sum_for_prop), size = prop*(23/sum_for_prop) , color = 'black', loc = 'center', rotation = 270)
    cbar.ax.yaxis.set_tick_params(color = 'black', size = prop*(5/sum_for_prop))
    cbar.outline.set_edgecolor('black')

    if 'used_in_Results' in kwargs:
        if kwargs['used_in_Results'] == True:
            cbar.ax.invert_yaxis() #Invert the axis tick labels of the colorbar
            
    #Setting elevation and Horizontal angle
    ax.view_init(el_angle, horz_angle)
    plt.show() #Show the plot

def plot_3d_Dust(name, X, Y, quality, color, x_range, y_range, z_min, l_Size, l_Dis, el_angle, horz_angle, lvls, z_upperlim, **kwargs):
            
    fig = plt.figure(figsize = (quality,quality))
    ax = plt.axes(projection= "3d")
    
    blackTheme(fig, ax)

    ax.set_title(name, fontproperties = 'Times New Roman', size = l_Size+30, color = 'white', y = 1, pad = -prop*(30/sum_for_prop))
    ax.set_ylabel("y-axis pixels", size = l_Size, labelpad = l_Dis, color = 'white')
    ax.set_xlabel("x-axis pixels", size = l_Size, labelpad = l_Dis, color = 'white')
    ax.set_zlabel("Photpix", size = l_Size, labelpad = l_Dis+5, color = 'white')
    ax.set_zlim(z_min,z_upperlim)
    ax.minorticks_on()
    
    #Function that converts sizes of x, y and z ticks to custom size
    tick_sizes(ax, l_Size/1.7)
    
    # ax.legend([fake2Dline], ["color = %s" % color], numpoints = 1)
    
    if 'Z' in kwargs: #If only one Z exists
        Z = kwargs['Z']
        
        sctt_1 = ax.scatter3D(X,Y,Z, c = Z , cmap = color, s = quality)
        
        set_contours(ax =ax, option = 2, cbarOutlinecol = 'white' ,
                     data_Arr = [X,Y], 
                     min_Arr = [x_range[0],y_range[0],lvls], 
                     max_Arr = [x_range[1],y_range[1],z_min], 
                     color = 'jet_r', l_Size = l_Size, fig = fig, Z = Z )
        #option = 1: Project 3d data on X axis alone
        #Option = 2: Project 3d data on X and Y axis
        #Option = 3: Project 3d data on X,Y and Z axis
        #information on the z-parametres are inverted. See logic on set_contours function.
        
        cbar = fig.colorbar(sctt_1, ax = ax, shrink = 0.4, aspect = 10)
        cbar.ax.tick_params(labelsize = l_Size/2, colors = 'white') #color bar tick labels smaller than graph axis labels
        cbar.set_label(kwargs['vert_cbar_name'], labelpad = prop*(25/sum_for_prop), size = prop*(23/sum_for_prop) , color = 'white', loc = 'center', rotation = 270)
        cbar.ax.yaxis.set_tick_params(color = 'white', size = prop*(5/sum_for_prop))
        cbar.outline.set_edgecolor('white')
            
    elif 'Z_1' in kwargs: #If multiple Z's exist
    
        Z_1, Z_2, Z_3 = kwargs['Z_1'], kwargs['Z_2'], kwargs['Z_3']
        
        k = 0 #Constant for choosing all data points where corresponding Z > constant
        
        #Filtering points
        points_1 = np.array([X[Z_1>k], Y[Z_1>k], Z_1[Z_1>k]])
        points_2 = np.array([X[Z_2>k], Y[Z_2>k], Z_2[Z_2>k]])
        points_3 = np.array([X[Z_3>k], Y[Z_3>k], Z_3[Z_3>k]])

        points = [points_1, points_2, points_3]
        
        # make grid of points
        x, y, z = np.mgrid[0:400:100j, 0:400:100j, 0:Levels:100j]

        tups = (x.ravel(), y.ravel(), z.ravel())
        # x-1D array on top of y 1D array. y-1D array on top of z-1D array. 
        positions = np.vstack(tups)
        zod = [-1,1] #For z-order to put contours in background
        n = 30 #number of levels for contour
        constant = 1

        col = ['g', 'y', 'b'] #Colors for scatter plot data points
        mark = ['o', '^', '^'] #Markers for scatter plot data points

        densities = [] #used to average contour plots from multiple datasets
        
        print('Attempts at plotting contours based on datasets provided:')
        print()
        for ind, p in enumerate(points):
            
            #Add scatter plot to figure
            ax.plot(p[0], p[1], p[2], mark[ind], c = col[ind], zorder = zod[1]+n**2, label = XYm_types[ind])

            if p.shape[1] == 0: #If there are no points where Z-axis is greater than 0
                print()
                print("Error: No points in dataset")
                print()
                continue #Dont set contours and their colorbars
            
            err_message = "The following error(s) have occurred for points involving the z-axis Z_%d" % (ind+1)
            try: #attempt the following
                # do kernel density estimation to get smooth estimate of distribution
                #get kernal probability from points
                kernel = scipy.stats.gaussian_kde(p)
                bw = kernel.factor / constant
                kernel.set_bandwidth(bw_method= bw)
            
            
            except np.linalg.LinAlgError as e_1:
                print(err_message) #State entirety of code DIDN'T run
                print(e_1)
                print('Hence contour calcuations cannot be computed')
                continue #Skip onto the next dataset and return densities
                
            except ValueError as e_2: #State entirety of code DIDN'T run
                print(err_message)
                print(e_2)
                print("Points are too few")
                continue #Skip onto the next dataset and return densities
                
            else: #if no errors
                print('DataSet %d contour calculations complete' % (ind+1)) #numbering system to keep track
                print() 
                density = np.reshape(kernel(positions).T, x.shape)  # now density is 100x100x100 
                densities.append(density)
                
        if np.array(densities).shape[0] == 1: #if only one is recorded density was recorded
            dens_avg = np.array(densities[0]) #use just that one density for contour plotting
        else:
            densities = np.array(densities)
            dens_avg = np.average(densities, axis = 0)#Get average density for contour plotting
        
        z_min_contour = z_min - ((z_upperlim-z_min)/4)*3
        
        cset = set_contours(ax =ax, option = 2, cbarOutlinecol = 'white',
                     data_Arr = [X,Y], min_Arr = [x_range[0],y_range[0],lvls], 
                     max_Arr = [x_range[1],y_range[1],z_min], color = 'jet_r', 
                     l_Size = l_Size, fig = fig, z_min_contour = z_min_contour,
                     Z_1 = points_1[2], Z_2 = points_2[2], Z_3 = points_3[2],
                     used_in_Results = True, zod = zod, n = n, density = dens_avg)
        
        #colorbar settings
        #all colorbars from cset_1. cset_2 and cset_3 are identical due to averaged density
        cbar_1 = plt.colorbar(cset[1], ax = ax, shrink = 0.4, aspect = 10)
        cbar_1.set_ticks(np.arange(0,1.1,0.1))
        cbar_1.ax.tick_params(labelsize = l_Size/2, colors = 'white') #color bar tick labels smaller than graph axis labels
        cbar_1.set_label(kwargs['vert_cbar_name'], labelpad = prop*(25/sum_for_prop), 
                         size = prop*(23/sum_for_prop) , color = 'white', 
                         loc = 'center', rotation = 270)
        cbar_1.ax.yaxis.set_tick_params(color = 'white', size = prop*(5/sum_for_prop))
        cbar_1.outline.set_edgecolor('white')
        cbar_1.minorticks_on()

        ax.set_zlim(z_min_contour, z_upperlim)
        ax.set_ylim(0, 500)
        ax.set_xlim(0, 500)
        plt.clim(0,1)
        
        ax.set_zlabel("Levels", size = l_Size, labelpad = l_Dis+5, color = 'white')
        ax.view_init(el_angle, horz_angle) #(<elevated angle>, <horizontal angle>)
        plt.legend(loc = 'upper right', bbox_to_anchor = (1.01, 0.9), markerscale = 700/sum_for_prop, 
                   fontsize = (l_Size*150)/sum_for_prop , framealpha = 0.2,
                   borderaxespad = -2, labelcolor = "white", frameon = False)
        plt.show()#plot everything in unison

def csv_export_query():
    outfileOpt = input("""
    Copy HA, OIII and SII Raw data into MESH within a csv file, repsectively?
    
    Y/N ?
    
    """)
    
    arrs_types = ['HA_raw', 'OIII_raw', 'SII_raw']
    
    
    #Taking all raw tuples from arrs_types and saving them in csv file
    if outfileOpt.lower() in agree:
    
        for i in range(len(arrs_types)):
            file = open(arrs_types[i] + ".csv", "w")  # 'w' means write
            writer = csv.writer(file) #Treat file as a csv file (commer seperated values)
            
            for j in arrs[i]:
                writer.writerow(list(j)) 
        
            file.close() #Once all csv writing is done, close the file
    elif outfileOpt.lower() in disagree:
        pass
    else:
        corrector()
    
def print_stat_dat(arrs):
    minToMax_arr = []   #Matrix needed to store 1D data for checking Max and Min 
                        #photons in particular array

    #Array storing string elements for ouptutting stat titles
    stat_titles = ["_____HA Stats________", "_____OIII Stats________", "_____SII Stats________" ]
    max_vals = [] #storing Maximum value of HA, OIII and SII into array, RESPECTIVELY
    min_vals = [] #storing Minimum value of HA, OIII and SII into array, RESPECTIVELY
    median_arr = [] #storing Median value of HA, OIII and SII into array, RESPECTIVELY
    modes_arr = [] #storing Modal(s) value of HA, OIII and SII into array, RESPECTIVELY
    stDev_arr = [] #storing standard Deviation value of HA, OIII and SII into array, RESPECTIVELY
    up_q_arr = []
    low_q_arr = []
    
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
        up_q_arr.append(up_q) , low_q_arr.append(low_q)
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
        if statDats.lower() in agree:
            print(stat_titles[x]) #print the current stat title
            print()
            print("Maximum photons in a pixel = ", maxim) #Max pixel value
            print("Minimum photons in a pixel = ", minim) #Min Pixel value
            print("Upper quartile = ", up_q) #Printing upper quartile info
            print("Lower Quartile = ", low_q) #Printing lower quartile info
            print("Median = ", med) #Getting median value
            print("Mode(s) = ", mode) #Getting modal value. Using multimode in case of two modes or more
            print("mean= %.3f " % mean)
            print("StDev = ", std) #Standard Deviation
            print()
        elif statDats.lower() in disagree:
            pass
        else: 
            corrector()
            
    return (min_vals, max_vals, stDev_arr, median_arr, modes_arr, up_q_arr, low_q_arr)
    
def show_unfilt_matrix_query(matrix_title, arrs):
    
    unfiltMTX = input("""
    Show unfiltered matrices of fit file images?

    Y/N ?
                   
    """)

    if unfiltMTX.lower() in agree:
        for x in range(len(arrs)): #Looping through length of arrs (starting from 0 to length-1)
            print(matrix_title[x]) #Print the title matrix before printing the matrix data
            print()
            print(arrs[x]) #Print the matrix 
            print()
    elif unfiltMTX.lower() in disagree:
        pass
    else: 
        corrector()
        

def main():
    
    """
    Converting PrimaryHDU's into numpy arrays by firstly extracting them from 
    FitsEctract.py package
    """
    arrs = [] #Storing numpy matrix of ImageHDU of HA, OIII and SII, respetively.
    names = ["Hydrogen Alpha", "Oxygen III", "Sulphur II"]

    for x in range(len(HDUs)):
        #HDUs[x][0] means the Primary HDU whilst HDUs[x][1] would have been ImageHDU
        arrs.append(np.array(HDUs[x][1].data))
        
        # Making sure to close each Fits file after accessing. 
        # Must come after converting the data to numpy array first
        HDUs[x].close()
        
    matrix_title = ["__________________HA array/matrix________________________", 
                    "__________________OIII array/matrix_________________________", 
                    "__________________SII array/matrix_________________________"]
    
    XYm_types = ['HA', 'OIII', 'SII']
    
    plotting_in_3d = input("""
    Show 3D plots of raw data

    Y/N ?

    """)

    if plotting_in_3d.lower() in agree:
        
        typ = int(input("""
        Choose from below:
        
            Hydrogen Alpha -> type the number 1
            Oxygen III     -> type the number 2
            Silicon II     -> type the number 3 
        
        
        """)) - 1
        
        if typ in [0,1,2]:
            X, Y, Z = get_coords(max_x = 400, max_y = 400, groupedIMGArray = arrs, arrayNum = typ)
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
                E_ang = 30
                colors = ['RdGy_r', 'hot', 'jet_r']
                for i in colors:
                    if i == 'hot': #Produce images to create horizontal rotation GIF
                        for H_ang in range(181,270,1): #Mid angle within this range is (226, 227, 1)
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
                        
                        for H_ang in range(181,270,1): #Mid angle within this range is (226, 227, 1)
                                                       #Actual good visible range -> (181, 270,1)

                            plot_contour_3d_graph(names[typ], X,Y, quality, color = i, 
                                                    x_range = [0,500], y_range= [0,500],
                                                    z_min = -300, l_Size = letterSize, 
                                                    l_Dis = letterDis, lvls = 256, 
                                                    el_angle = E_ang, horz_angle = H_ang,
                                                    z_upperlim = z_upperlim,
                                                    vert_cbar_name= "Photpix Colorbar", Z = Z)
                            
                    elif i == "jet_r": #Only make one image file
                        H_ang = 226
                        plot_contour_3d_graph(names[typ], X,Y,Z, quality, color = i, 
                                                x_range = [0,500], y_range= [0,500],
                                                z_min = -300, l_Size = letterSize, 
                                                l_Dis = letterDis, lvls = 256, 
                                                el_angle = E_ang, horz_angle = H_ang,
                                                z_upperlim = z_upperlim,
                                                vert_cbar_name= "Photpix Colorbar", Z = Z)
            elif typ == 1: #OIII data (Input by user was 2)
                            
                E_ang = 11
                for H_ang in range(181,270,1):
                    color = 'nipy_spectral'
                    plot_3d_Dust(names[typ], X, Y, Z, quality, color = color, 
                                x_range = [0,max_2d_plane], y_range = [0,max_2d_plane], 
                                z_min = 0, l_Size = letterSize, 
                                l_Dis = letterDis, el_angle = E_ang, 
                                horz_angle = H_ang, lvls = 256, z_upperlim = z_upperlim, 
                                vert_cbar_name= "Photpix Colorbar")
                    
            elif typ == 2: #SII data (Input by user was 3)

                color = 'gnuplot'
                
                z_upperlim = get_z_axis_max(Z)
                
                E_ang = 11
                for H_ang in range(181,270,1):
                    plot_3d_Dust(names[typ], X, Y, Z, quality, color, 
                                x_range = [0,max_2d_plane], y_range = [0,max_2d_plane], 
                                z_min = 0, l_Size = letterSize, 
                                l_Dis = letterDis, el_angle = E_ang, 
                                horz_angle = H_ang, lvls = 256, z_upperlim = z_upperlim,
                                vert_cbar_name= "Photpix Colorbar")
        else:
            corrector()
            
    elif plotting_in_3d.lower() in disagree:
        pass
    else:
        corrector()

    show_unfilt_matrix_query(matrix_title, arrs)
    
    # Statistical Data
    min_vals, max_vals, stDev_arr, median_arr, modes_arr, up_q_arr, low_q_arr = print_stat_dat(arrs)
    
    csv_export_query()

    print("_______________________________________________________________________________________________")

    scales = [] #Array holding constructed scales for HA, OIII and SII

    for x in range(len(max_vals)):
        scales.append((max_vals[x] - min_vals[x])/scF)

    XYm_gList = [] #List that holds tuples of (x,y,intensity level) for g_arr
    XYm_hList = [] #List that holds tuples of (x,y,intensity level) for h_arr
    XYm_iList = [] #List that holds tuples of (x,y,intensity level) for i_arr

    #array containing all XY_()List
    XYm_Lists = [XYm_gList, XYm_hList, XYm_iList]
    stat_data = (min_vals, max_vals, stDev_arr, median_arr, modes_arr, up_q_arr, low_q_arr)
    
    return XYm_Lists, XYm_types, arrs, names, max_vals, scales , stat_data

prop = 200 #Variable keeping all sizes of label elements in proportion
#Allows quality of graph to imporve whilst keeping everything else proportional
sum_for_prop = 190 #Sum of all the label sizes (including the padding of the graph)

###############################################################################
"""
Below is the part where I Look at high levels to relatively low intensity levels
The levels of intensity will be rated by the maximum and minimum values that
were previously collected.

All other lower levels of intensity are counted as negligible if user chooses 
a number of levels.

By increasing the scaling factor, the data is categorized in more levels.
By inputting the number of levels (starting from the highest level; Level 1), 
the data recorded will be categorized upto that level.
"""
###############################################################################

scF = get_scaling_Factor()
Levels = get_levels(scF)
        
XYm_Lists, XYm_types, arrs, names, max_vals, scales, stat_data = main()

#__________Kick-Start loading animation____________________
processing = True
t = threading.Thread(target=animate)
t.start()
#__________________________________________________________

fundamental_filt(XYm_Lists, arrs, max_vals, scales) #Fundamental Filtration

#__________Completing processing animation_________________
time.sleep(10)
processing = False
time.sleep(0.5)
#__________________________________________________________