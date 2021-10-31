from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np
 
points = np.random.rand(25, 2)
 
Plot = True
 
def min_convex(points):
    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_xticklabels([]) 
    ax1.set_yticklabels([])
    ax2.set_xticklabels([]) 
    ax2.set_yticklabels([])

    ax1.set_title("Punktemenge P")
    ax2.set_title("Convex Layer Decomposition von P")

    ax1.plot(points[:,0], points[:,1], 'o')
    ax2.plot(points[:,0], points[:,1], 'o')

    onion_layers = []    
    onion_points = [points]
    while len(points) > 2:
        layer = ConvexHull(points)
        onion_layers.append(layer)
        points = np.delete(points, layer.vertices, axis=0)
        onion_points.append(points)
    print(onion_points)
    count = -1
    if Plot == True:
        for layer in onion_layers:
            count = count+1
            for simplex in layer.simplices:
                ax2.plot(onion_points[count][simplex, 0], onion_points[count][simplex, 1], 'k-')  
    plt.show()

min_convex(points)