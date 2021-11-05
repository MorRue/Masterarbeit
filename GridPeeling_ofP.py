from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np
 

points = np.mgrid[-10:10.1:1, -10:10.1:1].reshape(2,-1).T
#points = np.random.rand(25, 2)
 
Plot = True
 
def min_convex(points):
    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_xticklabels([]) 
    ax1.set_yticklabels([])
    ax2.set_xticklabels([]) 
    ax2.set_yticklabels([])

    ax1.set_title("Ausgangsquadrat")
    ax2.set_title("Jedes fünfte Peeling des Quadrats")

    ax1.plot(points[:,0], points[:,1], 'o',ms=3)
    ax2.plot(points[:,0], points[:,1], 'o',ms=3)

    onion_layers = []    
    onion_points = [points]
    while len(points) > 2:
        layer = ConvexHull(points)
        onion_layers.append(layer)
        points = np.delete(points, layer.vertices, axis=0)
        onion_points.append(points)
    #print(onion_points)
    count = -1
    if Plot == True:
        for layer in onion_layers:
            count = count+1
            for simplex in layer.simplices:
                if(count%5 == 0):
                    if(count == 0):
                        ax1.plot(onion_points[count][simplex, 0], onion_points[count][simplex, 1], 'k-',linewidth=1.0)                     
                    ax2.plot(onion_points[count][simplex, 0], onion_points[count][simplex, 1], 'k-',linewidth=1.0)  
    plt.show()

min_convex(points)