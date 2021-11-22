from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np
 


###############################################################################
##                                                                           ##
##   Programm to calculate the convex-layer decomposition for a point set    ##
##              (was used to create pictures)                                ##
##                                                                           ##
###############################################################################


#points = np.mgrid[-10:10.1:1, -10:10.1:1].reshape(2,-1).T  #create grid to peel
points = np.random.rand(25, 2)  #create random point set to perform onvex-layer decomposition on
 
Plot = True
 
def cld(points): #performs the convex layer decomposition on points and displays it
    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_xticklabels([]) 
    ax1.set_yticklabels([])
    ax2.set_xticklabels([]) 
    ax2.set_yticklabels([])


    ax1.plot(points[:,0], points[:,1], 'o',ms=3)        #plot the starting set
    ax2.plot(points[:,0], points[:,1], 'o',ms=3)

    onion_layers = []    #all the CH's of the peelings
    onion_points = [points] #all vertices of the CH's
    while len(points) > 2:  #apply the grid peeling
        layer = ConvexHull(points)  #calculate CH
        onion_layers.append(layer)  #append CH
        points = np.delete(points, layer.vertices, axis=0)  #calculate vertices of CH
        onion_points.append(points) #append vertices
    #print(onion_points)
    count = -1
    n = 1   #show every n-th Peeling
    if Plot == True:
        for layer in onion_layers:  #go through all CH's
            count = count+1
            for simplex in layer.simplices: #go through all vertices of CH
                if(count%n == 0):                    
                    ax2.plot(onion_points[count][simplex, 0], onion_points[count][simplex, 1], 'black',linewidth=1.0)  
    ax1.set_title("Ausgangsmenge")
    if(n==1):
        ax2.set_title("Jede Schälung der Ausgangsmenge")
    else:
        ax2.set_title("Jede "+str(n)+"-te Schälung der Ausgangsmenge")

    plt.show()

cld(points)