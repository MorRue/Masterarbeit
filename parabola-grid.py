import math
from random import *
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np


#no clue how python works -> lets go global...

parabola_param = 0  #f(x)= (x-parabola_param)^2
highestx = 0        #number of calculated points
gridSize = 0        #self explanatory
gridparam = 0       #gridparam  = 1/gridsize and is needed to round the initial y values to the grid
rounder = 0         #rounder = the number of digits after the comma to round to the grid. -> necessary for the x and y values to be correct to avoid arithmetic floating point calculation errors
allPoints = []      #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
gradients = []      #gradients between the hullpoints


def roundToGrid(x):
    return math.ceil(x*gridparam)/gridparam


#TO-DO: avoid floating point arithmetic shit
#not now -> just for period correctness evaluation
def calc_distances(xValues,yValues):
    distbetween = []
    for i in range (0,len(xValues) -1):
        distance = math.sqrt( (xValues[i+1]-xValues[i]) ** 2 + (yValues[i+1]-yValues[i]) ** 2)
        distbetween.append(distance)
    return distbetween


def parabola_func(input,param):
    return round((input-param) ** 2,rounder*2)


def printstuff():
    print ("allPoints",  allPoints)
    print ("corners" , corners)
    print ("xdataHull",  xdataHull)
    print ("ydataHull",  ydataHull)
    print ("-------------------------------------")


#check every angle and delete point if necessary
def make_para_convex(xdata,ydata):
    i = 1
    while i  < len(xdata)-1:
        gradOne = math.atan2(round(ydata[i]-ydata[i-1],rounder),round(xdata[i]-xdata[i-1],rounder))
        gradTwo = math.atan2(round(ydata[i+1]-ydata[i],rounder),round(xdata[i+1]-xdata[i],rounder))
        if gradOne >= gradTwo:
            elementindex = int(round(gridparam*xdata[i],0))
            del xdata[i]
            del ydata[i]
            corners[elementindex]= 0
            if i != 1:
                i-=1
        else:
            i+=1
    return xdata,ydata


#fills the array allPoints with f(x) rounded up to the grid
#f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize} 
#corners is an array, which saves, if an element from allPoints is in the hull
#corners[i] == 1 -> ith element from allPoints is in the hull
#corners[i] == 0 -> ith element from allPoints is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(parabola_param, size, gridsize):
    global corners,allPoints,xdataHull,ydataHull,distances

    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        allPoints.append(roundToGrid(parabola_func(i*gridsize,parabola_param)))
        corners.append(1)
        xdataHull.append(round(i*gridsize,rounder))
        ydataHull.append(allPoints[i])   

    xdataHull,ydataHull = make_para_convex(xdataHull,ydataHull)     #make the hull convex by removing the "inner" points, 
    distances = calc_distances(xdataHull,ydataHull)

# makes one step of the gridPeeling and updates the hull values
def oneStep():
    global corners,allPoints,xdataHull,ydataHull,distances

    for i in range (0,len(corners)):
        if corners[i]==1:
            allPoints[i] = round(allPoints[i]+gridSize,rounder)
        corners[i]=1

    del xdataHull[:]
    del ydataHull[:]

    #add the mostright point of every x-value to the hull
    #pretty much just needed for the x=0 value, but yeah, better safe than sorry...
    for i in range (0,len(corners)-1):
        if allPoints[i] >= allPoints[i+1]:
            corners[i] = 0
        else:
            xdataHull.append(round(gridSize*i,rounder))
            ydataHull.append(allPoints[i])
    
    xdataHull,ydataHull = make_para_convex(xdataHull,ydataHull) #make the hull convex by removing the "inner" points 
    distances = calc_distances(xdataHull,ydataHull)



def main(gridVar,numX,numPeelings,printDebug,printPeriod,plot,plotPeriod,parabolaParam):

    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances
    parabola_param = parabolaParam
    numsteps = numPeelings       #number of gridpeelings
    gridparam = gridVar
    highestx = numX
    gridSize = roundToGrid(1/float(gridparam))
    rounder = int(math.ceil(math.log10(gridparam)))
    
    if printDebug==1:
        print("gridsize", gridSize)
        print("rounder",rounder)

    #this if-statement shall make a grid, but doesnt work for small gridsizes and looks awful..
    #-> made gridsize 0.1 in vizualization...
    if plot == 1 or plotPeriod==1:
        intervals = float(0.1) #Spacing between each line of the displayed grid -> NOT WORKING WTF
        fig,ax=plt.subplots()
        #ax.set_xticklabels([]) 
        #ax.set_yticklabels([])
        loc = plticker.MultipleLocator(base=intervals)
        loc.MAXTICKS= 694208142317
        ax.xaxis.set_major_locator(loc)
        ax.yaxis.set_major_locator(loc)
        ax.grid(which='major', axis='both', linestyle='-') 

    initialize(0,highestx,gridSize)
    if plot == 1:
        plt.scatter(xdataHull,ydataHull,s=10)
        plt.plot(xdataHull,ydataHull)
    if printDebug == 1:
        print("Initialized:")
        printstuff()
        print("-------------------------")

    for i in range (0,numsteps):
        oneStep()
        if plot == 1:
            plt.scatter(xdataHull,ydataHull,s=10)
            plt.plot(xdataHull,ydataHull)

        if printPeriod == 1:
            if(xdataHull[0]==0):
                print("----------------------")
                print(i,"xdataHull", xdataHull[:20])
                print(i,"ydataHull", ydataHull[:20])
                print("distances",distances[:20])
                #oneStep()
                if plotPeriod == 1:
                    plt.scatter(xdataHull,ydataHull,s=10)
                    plt.plot(xdataHull,ydataHull)
                #i+=1
                #print(i,"xdataHull", xdataHull[:100])
                #print("----------------------")

    if plot == 1 or plotPeriod==1:
        plt.show()

#printDebud ==1 -> Konsolenausdruck fuer Werte
#printPeriod ==1 -> moegliche Periode wird auf Konsole gedruckt
#plot ==1 -> Graphen werden geplottet
#works for sure with gridVar = 10^n, seems to work with m*gridvar = 10^n, no clue with other stuff...
#main(gridVar,numX,numPeelings,printDebug,printPeriod,plot,plotPeriod,parabola_param)
main(   10,   100,    0,        0,           0,      1,     0,           0)