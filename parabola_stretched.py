import csvStuff
import calc

import math
import os
import shutil
from random import *
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd


#first transforms the grid by stretching it to the standard grid
#the calculates the stretched a_one/a_two and calculates the period

def calculatePeriod():
    global a_one,a_two,b_one,b_two,g_one,g_two
    if b_one == 0:
        a_one_stretched = a_one * g_one
        a_two_stretched = a_two * g_two
        a_one_stretched, a_two_stretched = calc.bruchKuerzen(a_one_stretched,a_two_stretched)
        if(a_two_stretched%4 == 0):
            a_two_stretched = a_two_stretched*g_two*a_two*b_two
            return a_two_stretched/2
        else:
            a_two_stretched = a_two_stretched*g_two*a_two*b_two
            return a_two_stretched


'''
to make everything integers the whole thing gets stretched with
g_two*g_two*a_two
bzw. the whole space gets multiplied with the matrix

|g_two*g_two*a_two             0         |
|       0               g_two*g_two*a_two|

with:
f(x) = a_one/a_two * x^2
grid = g_one/g_two

'''

#x -> x * g_two * g_two * a_two * b_two
#x = input * g_one/g_two
#x -> input * g_one * g_two *a_two *b_two
def transformNormalToInt(input):
    return a_two*b_two * g_two*g_one*input

#grid -> grid * g_two * g_two * a_two *b_two
#grid = g_one/g_two
#grid -> g_one * g_two * a_two * b_two
def getGrid():
    return g_one*g_two*a_two * b_two


#returns f(x) but stretched and fitted to the grid
#f(x) =  a_one/a_two *(input * g_one/g_two)^2 + b_one/b_two * (input * g_one/g_two)
#f(x) -> a_one/a_two *(input * g_one/g_two)^2 *g_two *g_two *a_two * b_two +  b_one/b_two * (input * g_one/g_two) *g_two *g_two *a_two * b_two 
# = a_one * b_two * input^2 *g_one^2 + b_one * input * g_one * g_two * a_two
#
#1. case: f(x) = n*grid -> liegt auf dem grid und muss nicht "nach oben" angepasst werden
#
# 2. case: n*grid < f(x) < n+1 * grid
#mod = f(x) - n*grid -> f(x) - mod = n*grid
# -> f(x) - mod + grid = n+1 * grid

def parabola_func(input):
    mod = (input* input*a_one*b_two *g_one*g_one + input * a_two * b_one * g_one * g_two)%getGrid()
    if(mod == 0):
        return input* input*a_one*b_two *g_one*g_one + input * a_two * b_one * g_one * g_two
    else:
        return input* input*a_one*b_two *g_one*g_one + input * a_two * b_one * g_one * g_two + getGrid()-mod


#check every angle and delete point if necessary
def make_para_convex(xdata,ydata):
    i = 1
    while i  < len(xdata)-1:
        gradOne = math.atan2(ydata[i]-ydata[i-1],xdata[i]-xdata[i-1])
        gradTwo = math.atan2(ydata[i+1]-ydata[i],xdata[i+1]-xdata[i])
        if gradOne >= gradTwo:
            elementindex = int(round(xdata[i]/(a_two*g_two*g_one*b_two),0))
            del xdata[i]
            del ydata[i]
            corners[elementindex]= 0
            if i != 1:
                i-=1
        else:
            i+=1
    return xdata,ydata


def correctRightSide(startIndex,endIndex, xHull, yHull, distances, periodDistances,yAll):
    index = 0
    for i in range(startIndex,endIndex):
        distances[i]=periodDistances[index]
        xHull[i+1]=xHull[i]+distances[i]
        elementindex = int(round(xHull[i+1]/(a_two*g_two*g_one*b_two),0))
        if(elementindex<len(yAll)):
            yHull[i+1] = yAll[elementindex]
            index+=1
            if(index==len(periodDistances)):
                index = 0
        else:
            for j in range(i, len(distances)):
                del(distances[len(distances)-1])
                del(xHull[len(xHull)-1])
                del(yHull[len(yHull)-1])
            return xHull, yHull, distances
    return xHull, yHull, distances

def correctLeftSide(leftStartIndex, periodDistances, xHull, yHull, distances,yAll):
    index = len(periodDistances)-1
    for i in range(leftStartIndex,0,-1):
        if(xHull[i+1]-distances[i]>=0):
            distances[i]=periodDistances[index]
            xHull[i]=xHull[i+1]-distances[i]
            elementindex = int(round(xHull[i]/(a_two*g_two*g_one*b_two),0))
            yHull[i] = yAll[elementindex]
            index-=1
            if(index==-1):
                index = len(periodDistances)-1
        else:
            j=0
            while(j < i+1):
                del(xHull[0])
                del(yHull[0])
                del(distances[0])
                j+=1
            return xHull, yHull, distances
    return xHull, yHull, distances

def correctCorners(corners, xHull):
    for i in range(0,len(corners)):
        if(transformNormalToInt(i) in xHull):
            corners[i]=1
        else:
            corners[i]=0
    return corners

def correctHull(xHull,yHull,corners,distances,yAll):

    #
    #Decomment to write Logs
    #
    
    csvStuff.writePeeling(debugWriterX,"vorher","xHull",xHull)
    csvStuff.writePeeling(debugWriterY,"vorher","yHull",yHull)
    csvStuff.writePeeling(debugWriterDis,"vorher","distances",distances)
    


    start = int(len(distances)/3)
    periodDistances = calc.getPeriodDistances(start,len(distances),calculatePeriod(),distances)

    if(periodDistances == -1):
        return -1
    
    xHull, yHull, distances = correctRightSide(start+len(periodDistances),len(distances),xHull, yHull, distances, periodDistances,yAll)
    xHull, yHull, distances = correctLeftSide(start-1,periodDistances,xHull, yHull, distances,yAll)
    corners = correctCorners(corners, xHull)

    #
    #Decomment to write Logs
    #
    
    csvStuff.writePeeling(debugWriterX,"nachher","xHull",xHull)
    csvStuff.writePeeling(debugWriterY,"nachher","yHull",yHull)
    csvStuff.writePeeling(debugWriterDis,"nachher","distances",distances)
    

    return xHull,yHull,corners,distances


#fills the array allPoints with f(x) rounded up to the grid
#f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize} 
#corners is an array, which saves, if an element from allPoints is in the hull
#corners[i] == 1 -> ith element from allPoints is in the hull
#corners[i] == 0 -> ith element from allPoints is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(size):
    global corners,allPoints,xdataHull,ydataHull,distances,possiblePeriod
    del corners[:]
    del allPoints[:]
    del xdataHull[:]
    del ydataHull[:]
    del distances[:]
    del possiblePeriod[:]
    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        allPoints.append(parabola_func(i))
        corners.append(1)
        xdataHull.append(transformNormalToInt(i))
        ydataHull.append(allPoints[i])   

    xdataHull,ydataHull = make_para_convex(xdataHull,ydataHull)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,allPoints)
    for i in range(0,len(xdataHull)):
        possiblePeriod.append(xdataHull[i])

# makes one step of the gridPeeling and updates the hull values
def oneStep():
    global corners,allPoints,xdataHull,ydataHull,distances

    del xdataHull[:]
    del ydataHull[:]

    #TO-DO: make both loops in one loop!
    gridVar = getGrid()
    for i in range (0,len(corners)):
        if corners[i]==1:
            allPoints[i] = allPoints[i]+ gridVar
        corners[i]=1

    #add the mostright point of every x-value to the hull
    #pretty much just needed for the x=0 value, but yeah, better safe than sorry...
    for i in range (0,len(corners)-1):
        if allPoints[i] >= allPoints[i+1]:
            corners[i] = 0
        else:
            xdataHull.append(transformNormalToInt(i))
            ydataHull.append(allPoints[i])
    
    xdataHull,ydataHull = make_para_convex(xdataHull,ydataHull) #make the hull convex by removing the "inner" points 
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,allPoints)


def main(numX,numPeelings,printstep,plot,plotPeriod,a_one_in,a_two_in, b_one_in, b_two_in , g_one_in,g_two_in):
    periodReached = False
    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances,a_one,a_two,b_one, b_two,g_one,g_two, data_line
    a_one,a_two,b_one,b_two,g_one,g_two = a_one_in,a_two_in,b_one_in, b_two_in,g_one_in,g_two_in

    del data_line[:]
    data_line.append(a_one)
    data_line.append(a_two)
    data_line.append(b_one)
    data_line.append(b_two)
    data_line.append(g_one)
    data_line.append(g_two)

    numsteps = numPeelings       #number of gridpeelings
    highestx = numX
    


    #this if-statement shall make a grid, but doesnt work for small gridsizes and looks awful..
    #-> made gridsize 0.1 in vizualization...
    
    if plot == 1 or plotPeriod==1:
        intervals = float(getGrid()) #Spacing between each line of the displayed grid -> NOT WORKING WTF
        fig,ax=plt.subplots()
        #ax.set_xticklabels([]) 
        #ax.set_yticklabels([])
        loc = plticker.MultipleLocator(base=intervals)
        loc.MAXTICKS= 694208142317
        ax.xaxis.set_major_locator(loc)
        ax.yaxis.set_major_locator(loc)
        ax.grid(b= True, which='major', axis='both', linestyle='-')
    

    initialize(highestx)

    
    if(printstep==1):
        print("---------------------- Initial ----------------------")
        print("xdataHull", xdataHull[:20])
        print("ydataHull", ydataHull[:20])
        print("distances",distances[:20],'\n')
        
    if plot == 1 or plotPeriod ==1:
        #plt.scatter(xdataHull,ydataHull,s=10)
        #plt.plot(xdataHull,ydataHull)
        plt.scatter(xdataHull[:10],ydataHull[:10],s=10)
        plt.plot(xdataHull[:10],ydataHull[:10])
    

    for i in range (1,numsteps):
        oneStep()
        

        if printstep == 1:
            print("---------------------- Peeling",i+1,"----------------------")
            print("xdataHull", xdataHull)
            print("ydataHull", ydataHull)
            print("distances",distances,'\n')

        if plot == 1:
            plt.scatter(xdataHull[:10],ydataHull[:10],s=10)
            plt.plot(xdataHull[:10],ydataHull[:10])
            #plt.scatter(xdataHull,ydataHull,s=10)
            #plt.plot(xdataHull,ydataHull)
        

        if(xdataHull[0]==0):
            if(xdataHull==possiblePeriod):
                if(periodReached == True):
                    data_line.append(i-data_line[len(data_line)-1])

                    #
                    #Decomment to write Logs
                    #                    
                    globalWriter.writerow(data_line)

                    break
                periodReached = True
                data_line.append(i)

            else:
                del possiblePeriod[:]
                for i in range(0,len(xdataHull)):
                    possiblePeriod.append(xdataHull[i])
     
    if plot == 1 or plotPeriod==1:
        '''
        # 100 linearly spaced numbers
        mostrightx = int(xdataHull[10]/a_two)
        x = np.linspace(xdataHull[0],mostrightx,10)
        y = a_one*(x**2)*b_two + b_one * x * a_two 
        x = a_two*x*b_two
        plt.plot(x,y, 'r', color = '0')
        '''
        plt.show()




allPoints = []      #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
gradients = []      #gradients between the hullpoints
possiblePeriod = []


#a_one | a_two | b_one | b_two | g_one | g_two | StepsToVerticalPeriod | StepsToNewVerticalPeriod
data_line = []      #line which gets written in CSV

# PARABOLA COEFFICIENTS
a_one = 1           #a_one , a_two , b_one and b_two are the Nenner(two) and Zaehler(one) from f(x) = ax^2 + bx
a_two = 2
b_one = 0
b_two = 1            # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 1

#THEORETICALSTUFF
highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
numPeelings = 100000000

#VIEWSTUFF
printstep = 0      #printstep == 1 -> jeder Schritt wird geprintet
plot = 0            #plot ==1 -> Graphen werden geplottet
plotPeriod = 0      #plotPeriod == 1 -> nur Graphen mit xdata[0] == 0 werden geplottet

#main(highestx,numPeelings,printstep, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)





#For CSV stuff
periodReached  = False
path = "../All Logs/Logs220621/"


os.mkdir(path)

globalWriter = csvStuff.createWriter(path+"LogAll.csv")
header = ["a_one","a_two","b_one","b_two","g_one","g_two","steps til first","steps til second period"]
globalWriter.writerow(header)
#shutil.rmtree("LogsNew")
os.mkdir(path+"Logs")


k=1
while(k<1000):
    g_two = k
    for j in range(1,20):
        for i in range(j,20):
            a_one = j
            a_two = i
            highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
            if(calc.ggT(a_one,a_two)!=1):
                continue
            name = path+"Logs/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)
            print(name)
            os.mkdir(name)
            debugWriterX = csvStuff.createWriter(name+"/debuggerX.csv")
            debugWriterY = csvStuff.createWriter(name+"/debuggerY.csv")
            debugWriterDis = csvStuff.createWriter(name+"/debuggerDis.csv")

            main(highestx,numPeelings,printstep, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)
    k = k*10


