import csvStuff
import calc
import calcVerticalDis

import time
import math
import os
import shutil
from random import *
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd
import cProfile

#first transforms the grid by stretching it to the standard grid
#then calculates the stretched a_one/a_two and calculates the period

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
    else:
        a_one_stretched = a_one * g_one
        a_two_stretched = a_two * g_two
        a_one_stretched, a_two_stretched = calc.bruchKuerzen(a_one_stretched,a_two_stretched)

        b_one_stretched = b_one #* g_one
        b_two_stretched = b_two #* g_two
        b_one_stretched, b_two_stretched = calc.bruchKuerzen(b_one_stretched,b_two_stretched)
        periodCase = getPeriodCase(a_two_stretched,b_two_stretched)
        if(periodCase==0):
            print("Problem")
            return
        period = getPeriod(periodCase,a_two_stretched,b_two_stretched)
        #period_stretched =2* period*g_two*a_two*b_two  # 2* because there is a problem
        period_stretched =period*g_two*a_two*b_two

        return period_stretched 

def getHorizontalPeriod(a,b):
    periodCase = getPeriodCase(a,b)
    return getPeriod(periodCase,a,b)


def getPeriod(periodCase,a, b):
    if(periodCase=='a'):
        period = calc.getInt(a*b/calc.ggT(a,b))
    elif(periodCase=='b'):
        a_half = calc.getInt(a/2)
        period =calc.getInt(a_half*b/calc.ggT(a_half,b))
    elif(periodCase=='c'):
        period = calc.getInt(a*b/calc.ggT(a,b))
    elif(periodCase=='d'):
        period = calc.getInt(a*b/calc.ggT(a,b))
    elif(periodCase=='e'):
        a_half = calc.getInt(a/2)
        period = calc.getInt(a_half*b/calc.ggT(a,b))
    elif(periodCase=='f'):
        a_half = calc.getInt(a/2)
        period = a_half
    return period   

def getPeriodCase(a,b):
    if(a%2!=0):
        return 'a'
    if(a%4==0):
        return 'b'
    if(a%2==0 and a%4!=0 and b%2 != 0):
        return 'c'
    if(a%2==0 and a%4!=0 and b%4 == 0):
        return 'd'
    if(a%2==0 and a%4!=0 and b%2 == 0 and b%4 != 0):
        return 'e'
    if(a == b and a%2 == 0 and a%4 != 0):
        return 'f'
    return 0


'''
to make everything integers the whole thing gets stretched with
g_two*g_two*a_two
bzw. the whole space gets multiplied with the matrix

|g_two*g_two*a_two*b_two             0         |
|       0               g_two*g_two*a_two*b_two|

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


#returns the real grid
def getRealGrid():
    return g_one/float(g_two)

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


#receives set of points and returns bottom convex hull
def make_para_convex(xdata,ydata):
    xdataHull = []
    ydataHull = []

    xdataHull.append(xdata[0])
    ydataHull.append(ydata[0])
    l = 0
    for k in range(1,len(xdata)):
        if(l>=1):
            gradOne = math.atan2(ydataHull[l]-ydataHull[l-1],xdataHull[l]-xdataHull[l-1])
            gradTwo = math.atan2(ydata[k]-ydataHull[l],xdata[k]-xdataHull[l])
            while(l>=1 and gradOne >= gradTwo):
                xdataHull.pop()
                ydataHull.pop()
                l -= 1
                if(l>=1):
                    gradOne = math.atan2(ydataHull[l]-ydataHull[l-1],xdataHull[l]-xdataHull[l-1])
                    gradTwo = math.atan2(ydata[k]-ydataHull[l],xdata[k]-xdataHull[l])
        l += 1
        xdataHull.append(xdata[k])
        ydataHull.append(ydata[k])
    return xdataHull,ydataHull


def correctRightSide(startIndex,endIndex, xHull, yHull, distances, periodDistances,yAll):
    index = 0
    for i in range(startIndex,endIndex):
        #if(distances[i]!=periodDistances[index]):
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
                '''
                distances.pop()
                xHull.pop()
                yHull.pop()
                '''
            return xHull, yHull, distances
    return xHull, yHull, distances

def correctLeftSide(leftStartIndex, periodDistances, xHull, yHull, distances,yAll):
    index = len(periodDistances)-1
    for i in range(leftStartIndex,-1,-1):
        #if(distances[i]!=periodDistances[index]):
        if(xHull[i+1]-periodDistances[index]>=0):
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
                '''
                xHull.pop(0)
                yHull.pop(0)
                distances.pop(0)
                '''
                j+=1
            return xHull, yHull, distances
    return xHull, yHull, distances

def correctCorners(corners, xHull):
    #gridVar = getGrid()

    for i in range(0,len(corners)):
        corners[i]=0

    for i in range(0,len(xHull)):
        elementindex = int(round(xHull[i]/(a_two*g_two*g_one*b_two),0))
        corners[elementindex]=1
 
    return corners

def correctHull(xHull,yHull,corners,distances,yData):

    
    #
    #Decomment to write Logs
    #
    
    csvStuff.writePeeling(debugWriterX,"vorher","xHull",xHull)
    csvStuff.writePeeling(debugWriterY,"vorher","yHull",yHull)
    csvStuff.writePeeling(debugWriterDis,"vorher","distances",distances)
    csvStuff.writePeeling(debugWriterCorners,"vorher","Corners",corners)



    start = int(len(distances)/3)
    periodDistances = calc.getPeriodDistances(start,len(distances),calculatePeriod(),distances)

    if(periodDistances == -1):
        print("problem")
        return -1
    
    xHull, yHull, distances = correctRightSide(start+len(periodDistances),len(distances),xHull, yHull, distances, periodDistances,yData)
    xHull, yHull, distances = correctLeftSide(start-1,periodDistances,xHull, yHull, distances,yData)
    corners = correctCorners(corners, xHull)

    
    #
    #Decomment to write Logs
    #
    
    csvStuff.writePeeling(debugWriterX,"nachher","xHull",xHull)
    csvStuff.writePeeling(debugWriterY,"nachher","yHull",yHull)
    csvStuff.writePeeling(debugWriterDis,"nachher","distances",distances)
    csvStuff.writePeeling(debugWriterCorners,"nachher","Corners",corners)
    

    return xHull,yHull,corners,distances


#fills the array yData with f(x) rounded up to the grid
#f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize} 
#corners is an array, which saves, if an element from yData is in the hull
#corners[i] == 1 -> ith element from yData is in the hull
#corners[i] == 0 -> ith element from yData is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(size):
    global corners,yData,xdataHull,ydataHull,distances,possiblePeriodX,xData
    '''
    del corners[:]
    del yData[:]
    del xdataHull[:]
    del ydataHull[:]
    del distances[:]
    del possiblePeriodX[:]
    
    '''
    corners =[]
    yData = []
    xData = []
    xdataHull = []
    ydataHull = []
    distances = []
    possiblePeriodX = []
    
    #gridVar = getGrid()
    stretchedPeriod = calculatePeriod()
    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        corners.append(0)
        xData.append(transformNormalToInt(i))
        yData.append(parabola_func(i))
        if(transformNormalToInt(i)%math.ceil(stretchedPeriod/2) == 0 and transformNormalToInt(i)!= 2*math.ceil(stretchedPeriod/2) and transformNormalToInt(i)!= 4*math.ceil(stretchedPeriod/2) and transformNormalToInt(i)!= 6*math.ceil(stretchedPeriod/2) and i!=0):
            xdataHull.append(transformNormalToInt(i))
            ydataHull.append(parabola_func(i))
            corners.pop()
            corners.append(1)


    #xdataHull,ydataHull = make_para_convex(xData,yData)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)



#plots the x and y Values stretched back to the Z2 
#x -> x/(g_two^2 * a_two * b_two)

def plotRealValues(xValues,yValues):
    xPlot = []
    yPlot = []
    for i in range(0,len(xValues)):
        x = xValues[i]/(g_two*g_two*a_two*b_two)
        y = yValues[i]/(g_two*g_two*a_two*b_two)
        xPlot.append(x)
        yPlot.append(y)
    disPlot = calc.calc_distances_one(xPlot)
    '''
    debugWriterX.writerow(xPlot)
    debugWriterY.writerow(yPlot)
    debugWriterDis.writerow(disPlot)
    '''
    plt.scatter(xPlot,yPlot,s=10)
    plt.plot(xPlot,yPlot)
    #plt.scatter(xPlot[:20],yPlot[:20],s=10)
    #plt.plot(xPlot[:20],yPlot[:20])


def plotRealValuesBlack(xValues,yValues):
    xPlot = []
    yPlot = []
    for i in range(0,len(xValues)):
        x = xValues[i]/(g_two*g_two*a_two*b_two)
        y = yValues[i]/(g_two*g_two*a_two*b_two)
        xPlot.append(x)
        yPlot.append(y)
    disPlot = calc.calc_distances_one(xPlot)
    '''
    debugWriterX.writerow(xPlot)
    debugWriterY.writerow(yPlot)
    debugWriterDis.writerow(disPlot)
    '''
    plt.scatter(xPlot,yPlot,s=100,color = 'black')
    plt.plot(xPlot,yPlot,color = 'black')


# makes one step of the gridPeeling and updates the hull values
def oneStep():
    global corners,yData,xdataHull,ydataHull,distances,xData
    '''
    del xdataHull[:]
    del ydataHull[:]
    '''
    xdataHull = []
    ydataHull = []
    
    #TO-DO: make both loops in one loop?
    gridVar = getGrid()
    
    for i in range (0,len(corners)):
        if corners[i]==1:
            yData[i] = yData[i]+ gridVar

        corners[i]=1
 
    
    xdataHull,ydataHull = make_para_convex(xData,yData) #make the hull convex by removing the "inner" points 
    corners = correctCorners(corners,xdataHull)
    #debugWriterCorners.writerow(corners[int(len(corners)/3):2*int(len(corners)/3)])
    distances = calc.calc_distances_one(xdataHull)
    #xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData)

def testPeriod(ydata,possibleY):
    difference = ydata[0]-possibleY[0]
    for i in range(0,len(ydata)):
        if(possibleY[i]+difference != ydata[i]):
            #print(possibleY[i]-ydata[i])
            return False
    return True
    



def mainTwo(numX,numPeelings,plot,plotPeriod,a_one_in,a_two_in, b_one_in, b_two_in , g_one_in,g_two_in):
    periodReached = False
    count = 1
    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances,a_one,a_two,b_one, b_two,g_one,g_two, data_line,possiblePeriodCorners
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
        intervals = float(getGrid()) #Spacing between each line of the displayed grid 
        #intervals = float(getRealGrid())
        fig,ax=plt.subplots()
        #ax.set_xticklabels([]) 
        #ax.set_yticklabels([])
        
        #locx = plticker.MultipleLocator(base=1)
        #locx.MAXTICKS= 694208142317
        #locy = plticker.MultipleLocator(base=1)
        #locy.MAXTICKS= 694208142317
        
        #ax.xaxis.set_major_locator(locx)
        #ax.yaxis.set_major_locator(locy)
        
        plt.gca().xaxis.grid(False)
        ax.grid(b= False, which='both', axis='both', linestyle='-',zorder =10)
    

    initialize(highestx)
    print("period:",calculatePeriod()/a_two/b_two)

    #print("initialized")    
    #print(xdataHull)
    #print(ydataHull)
        
    if plot == 1 or plotPeriod ==1:
        #plotSecondHalf(xdataHull,ydataHull)

        plotRealValuesBlack(xdataHull,ydataHull)
        #plotRealValuesTranslate(xdataHull,ydataHull,0)

    

    for i in range(0,numsteps):
    
    #i=0
    #while(True):
        #i = i+1
        oneStep()

        if plot == 1:
            #plotSecondHalf(xdataHull,ydataHull)
            plotRealValues(xdataHull,ydataHull)
            #plotRealValuesTranslate(xdataHull,ydataHull,0.2*i)

        
        count += 1   
        if(corners[int(len(corners)/3):2*int(len(corners)/3)] == possiblePeriodCorners):
            if(periodReached == True):
                data_line.append(i-data_line[len(data_line)-1])
                data_line.append(getHorizontalPeriod(a_two,b_two))
                print("-------Period found!--------")
                #
                #Decomment to write Logs
                #                    
                #globalWriter.writerow(data_line)

                break
            periodReached = True
            #print(ydataHull[0]/(b_two*a_two))
            data_line.append(i)
        elif(math.ceil(math.log2(count)) == math.log2(count) and periodReached == False):
            possiblePeriodCorners = corners[int(len(corners)/3):2*int(len(corners)/3)]
            
    if(i == numsteps-1):
        data_line.append(0)
        data_line.append(0)
        data_line.append(0)
        print("-------Period not found!--------")
        #
        #Decomment to write Logs
        #                    
        #globalWriter.writerow(data_line)


               
     
    if plot == 1 or plotPeriod==1:
        
        mostrightx = int(xdataHull[-1]/a_two/b_two)
        leftrightx = int(xdataHull[int(len(xdataHull)/3)]/a_two/b_two)

        x = np.linspace(leftrightx,mostrightx,1000)
        y = a_one*(x**2)/a_two + b_one * x /b_two 
        #x = a_two*x*b_two
        #plt.plot(x,y, 'r', color = '0')
        
        plt.show()





yData = []      #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xData = []          # -1 if point is in hull, x value instead
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
gradients = []      #gradients between the hullpoints
possiblePeriodCorners = []



#a_one | a_two | b_one | b_two | g_one | g_two | StepsToVerticalPeriod | StepsToNewVerticalPeriod
data_line = []      #line which gets written in CSV

# PARABOLA COEFFICIENTS
a_one = 1            #a_one , a_two , b_one and b_two are the Nenner(two) and Zaehler(one) from f(x) = ax^2 + bx
a_two = 2
b_one = 5
b_two = 9        # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 1

#THEORETICALSTUFF
highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
if(highestx<100):
    highestx = 100
numPeelings = 200
periodReached  = False


#VIEWSTUFF
printstep = 0      #printstep == 1 -> jeder Schritt wird geprintet
plot = 1         #plot ==1 -> Graphen werden geplottet
plotPeriod = 0      #plotPeriod == 1 -> nur Graphen mit xdata[0] == 0 werden geplottet


#debugWriterX = csvStuff.createWriter("../debuggerX.csv")
#debugWriterY = csvStuff.createWriter("../debuggerY.csv")
#debugWriterDis = csvStuff.createWriter("../debuggerDisAll.csv")


mainTwo(highestx,numPeelings, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)

#cProfile.run('main(highestx,numPeelings,printstep, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)')

'''

#For CSV stuff
path = "../All Logs/Investigate Unglatt/"


os.mkdir(path)

globalWriter = csvStuff.createWriter(path+"LogAll.csv")
headerGlob = ["a_one","a_two","b_one","b_two","g_one","g_two","steps til first","steps til second period","horizontal Period","last_x_min","lastMinDis","last_x_max","lastMaxDis"]
globalWriter.writerow(headerGlob)

distanceWriter = csvStuff.createWriter(path+"Distances.csv")
headerDis = ["a_one","a_two","b_one","b_two","Peeling","x_min","dis_min","x_max","dis_max"]
distanceWriter.writerow(headerDis)

os.mkdir(path+"Logs")

for j in range(1,20,20):
    for i in range(j,20,1):
        for l in range(0,10,1):
            for m in range(abs(l),10,1):
                a_one = j
                a_two = i
                b_one = l

                b_two = m
                if(b_one == 0 and b_two!=1):
                    continue

                highestx = int(20*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
                
                if(highestx<100):
                    highestx=100
                if(calc.ggT(a_one,a_two)!=1):
                    continue
                if(calc.ggT(abs(b_one),abs(b_two))!=1):
                    continue
                name = path+"Logs/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)
                print(name)
                os.mkdir(name)
                debugWriterX = csvStuff.createWriter(name+"/debuggerX.csv")
                debugWriterY = csvStuff.createWriter(name+"/debuggerY.csv")
                debugWriterDis = csvStuff.createWriter(name+"/debuggerDis.csv")
                debugWriterCorners = csvStuff.createWriter(name+"/debuggerCorners.csv")

                mainTwo(highestx,numPeelings, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)

'''