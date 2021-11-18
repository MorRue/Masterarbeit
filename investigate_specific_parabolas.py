import cProfile
import math
import os
import shutil
import time
from random import *

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from numpy.lib.function_base import average, diff

import calc
import calcVerticalDis
import csvStuff

#first transforms the grid by stretching it to the standard grid
#then calculates the stretched a_one/a_two and calculates the period

def calculatePeriod():
    global a_one,a_two,b_one,b_two,g_one,g_two  #parabola coefficients and grid variables
    
    #case that there is no linear part in the parabola function
    if b_one == 0:                              
        a_one_stretched = a_one * g_one         #stretch parabola to standard grid
        a_two_stretched = a_two * g_two         #

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


def initializeDif(corners,xData,yData):
    dif = []
    count = 0
    for i in range(0,len(corners)):
        if(corners[i]==1):
            if(count != 0 and count+1<len(yData)):
                gradOne = (int(yData[count])-int(yData[count-1]))/(int(xData[count])-int(xData[count-1]))
                gradTwo = (int(yData[count+1])-int(yData[count]))/(int(xData[count+1])-int(xData[count]))
                dif.append(gradTwo-gradOne)
            else:
                dif.append('x')
            count +=1
        else:
            dif.append('x')
    return dif


            
#receives set of points and returns bottom convex hull
def make_para_convex(xdata,ydata):
    xdataHull = []
    ydataHull = []

    xdataHull.append(xdata[0])
    ydataHull.append(ydata[0])
    l = 0
    for k in range(1,len(xdata)):
        if(l>=1):
            gradOne = (ydataHull[l]-ydataHull[l-1]) * (xdata[k]-xdataHull[l])
            gradTwo = (ydata[k]-ydataHull[l]) * (xdataHull[l]-xdataHull[l-1])
            while(l>=1 and gradOne >= gradTwo):
                xdataHull.pop()
                ydataHull.pop()
                l -= 1
                if(l>=1):
                    gradOne = (ydataHull[l]-ydataHull[l-1]) * (xdata[k]-xdataHull[l])
                    gradTwo = (ydata[k]-ydataHull[l]) * (xdataHull[l]-xdataHull[l-1])

        l += 1
        xdataHull.append(xdata[k])
        ydataHull.append(ydata[k])
    return xdataHull,ydataHull



#receives the calculated corners of the convex hull (xHull,yHull) and the distances inbetween the 
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
    
    #csvStuff.writePeeling(debugWriterX,"vorher","xHull",xHull)
    #csvStuff.writePeeling(debugWriterY,"vorher","yHull",yHull)
    csvStuff.writePeeling(debugWriterCorners,"vorher","Corners",corners)
    #csvStuff.writePeeling(debugWriterDis,"vorher","dis",distances)


    start = int(len(distances)/3)
    periodDistances = calc.getPeriodDistances(start,len(distances),calculatePeriod(),distances)

    if(periodDistances == -1):
        print("problem")
        return -1
    
    xHull, yHull, distances = correctRightSide(start+len(periodDistances),len(distances),xHull, yHull, distances, periodDistances,yData)
    xHull, yHull, distances = correctLeftSide(start-1,periodDistances,xHull, yHull, distances,yData)
    corners = correctCorners(corners, xHull)
    #dif = initializeDif(corners,xHull,yHull)
    #dis_all = calcVerticalDis.getAllMaxDistance(a_one,a_two,b_one,b_two,xHull[:int(len(xHull)/3)],yHull[:int(len(xHull)/3)])

    #
    #Decomment to write Logs
    #
    #csvStuff.writePeeling(debugWriterX,"nachher","xHull",xHull)
    #csvStuff.writePeeling(debugWriterY,"nachher","yHull",yHull)
    csvStuff.writePeeling(debugWriterCorners,"nachher","Corners",corners)    
    #csvStuff.writePeeling(debugWriterDis,"nachher","dis",distances)



    '''
    debugWriterX.writerow(xHull)
    debugWriterY.writerow(yHull)
    #debugWriterDis.writerow(dis_all)
    debugWriterCorners.writerow(corners)
    #debugWriterGrad.writerow(dif)
    '''
    #vectors = []
    #for i in range(1,len(xHull)):
    #    vectors.append([(xHull[i]-xHull[i-1])/(a_two*b_two),(yHull[i]-yHull[i-1])/(a_two*b_two)])

    #vectorWriter.writerow(vectors)
    return xHull,yHull,corners,distances


#fills the array yData with f(x) rounded up to the grid
#f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize} 
#corners is an array, which saves, if an element from yData is in the hull
#corners[i] == 1 -> ith element from yData is in the hull
#corners[i] == 0 -> ith element from yData is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(size):
    global corners,yData,xdataHull,ydataHull,distances,possiblePeriodX,possiblePeriodY,xData
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
    possiblePeriodY = []

    #gridVar = getGrid()

    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        corners.append(1)
        xData.append(transformNormalToInt(i))
        yData.append(parabola_func(i))


    xdataHull,ydataHull = make_para_convex(xData,yData)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData)
    for i in range(0,len(xdataHull)):
        possiblePeriodX.append(xdataHull[i])
        possiblePeriodY.append(ydataHull[i])

def getAverageVerticalTranslation(MinVerticalDis):
    averageTranslation = []
    for i in range(1,len(MinVerticalDis)):
        averageTranslation.append(MinVerticalDis[i]-MinVerticalDis[i-1])
    return averageTranslation


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
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData)


def testPeriod(ydata,possibleY):
    difference = ydata[0]-possibleY[0]
    for i in range(0,len(ydata)):
        if(possibleY[i]+difference != ydata[i]):
            print(difference)
            print(possibleY[i]-ydata[i])
            return False
    return True



def mainTwo(numX,numPeelings,plot,plotPeriod,a_one_in,a_two_in, b_one_in, b_two_in , g_one_in,g_two_in):
    periodReached = False
    count = 0
    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances,a_one,a_two,b_one, b_two,g_one,g_two, data_line
    a_one,a_two,b_one,b_two,g_one,g_two = a_one_in,a_two_in,b_one_in, b_two_in,g_one_in,g_two_in
    
    allMindistances = []
    allMaxdistances = []

    periodMaxdistances = []
    periodMindistances = []
    del data_line[:]
    data_line.append(a_one)
    data_line.append(a_two)
    data_line.append(b_one)
    data_line.append(b_two)
    data_line.append(g_one)
    data_line.append(g_two)
    
    numsteps = numPeelings       #number of gridpeelings
    highestx = numX
    
    times = []

    #this if-statement shall make a grid, but doesnt work for small gridsizes and looks awful..
    #-> made gridsize 0.1 in vizualization...
    
    if plot == 1 or plotPeriod==1:
        intervals = float(getGrid()) #Spacing between each line of the displayed grid 
        #intervals = float(getRealGrid())
        fig,ax=plt.subplots()
        #ax.set_xticklabels([]) 
        #ax.set_yticklabels([])
        
        locx = plticker.MultipleLocator(base=1)
        #locx.MAXTICKS= 694208142317
        locy = plticker.MultipleLocator(base=1)
        #locy.MAXTICKS= 694208142317
        
        ax.xaxis.set_major_locator(locx)
        ax.yaxis.set_major_locator(locy)
        
        plt.gca().xaxis.grid(False)
        ax.grid(b= False, which='both', axis='both', linestyle='-',zorder =10)
    
    timeStart = time.time()
    initialize(highestx)
    
    timeEnd = time.time()
    timeDiff = timeEnd-timeStart
    times.append(timeDiff)
    
    x_max,dis_max = calcVerticalDis.getMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
    x_min, dis_min = calcVerticalDis.getMinDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
    dis_max = dis_max-dis_min
    line = [x_min,dis_min,x_max,dis_max]
    distanceWriter.writerow(line)

    allMindistances.append(dis_min)
    allMaxdistances.append(dis_max)

    
    #print("initialized")    

    
    i=0
    while(True):
        i = i+1
        timeStart = time.time()
        oneStep()
        timeEnd = time.time()
        timeDiff = timeEnd-timeStart
        times.append(timeDiff)
        
        x_max,dis_max = calcVerticalDis.getMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
        x_min, dis_min = calcVerticalDis.getMinDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
        dis_max = dis_max-dis_min
        line = [x_min,dis_min,x_max,dis_max]
        distanceWriter.writerow(line)

        #vertical Velocity
        allMindistances.append(dis_min)
        allMaxdistances.append(dis_max)

        if(periodReached==True):
            periodMindistances.append(dis_min)
            periodMaxdistances.append(dis_max)

        
        if(xdataHull[0]==0):

            count = count+1
            if(xdataHull==possiblePeriodX and testPeriod(ydataHull,possiblePeriodY)):
                if(periodReached == True):
                    data_line.append(i-data_line[len(data_line)-1])
                    
                    #print("vertikale Periode:",data_line[-1])

                    data_line.append(getHorizontalPeriod(a_two,b_two))
                    timeAverage = sum(times)/len(times)
                    data_line.append(timeAverage)
                    
                    allVerticalTranslation = getAverageVerticalTranslation(allMindistances)
                    AllperiodVerticalTranslation = getAverageVerticalTranslation(periodMindistances)
                    if(len(AllperiodVerticalTranslation)!=0):
                        periodVerticalTranslation =sum(AllperiodVerticalTranslation)/len(AllperiodVerticalTranslation)
                    else:
                        periodVerticalTranslation = 1
                    averageVerticalDis = sum(allVerticalTranslation)/len(allVerticalTranslation)
                    averageTubeThickness = sum(allMaxdistances)/(len(allMaxdistances))
                    maxTubeThickness = max(allMaxdistances)
                    minTubeThickness = min(allMaxdistances)
                    maxTubeThicknessPeriod =  max(periodMaxdistances)
                    averageTubeThicknessPeriod = sum(periodMaxdistances)/(len(periodMaxdistances))
                    data_line.append(averageVerticalDis)
                    #data_line.append(periodVerticalTranslation)
                    data_line.append(averageTubeThickness)
                    data_line.append(minTubeThickness)
                    data_line.append(maxTubeThickness)
                    data_line.append(averageTubeThicknessPeriod)
                    data_line.append(periodVerticalTranslation)
                    data_line.append(maxTubeThicknessPeriod)
                    
                    #print("-------Period found!--------")
                    #data_line.extend([x_min,dis_min,x_max,dis_max])
                    #
                    #Decomment to write Logs
                    #                    
                    globalWriter.writerow(data_line)

                    break
                #periodMindistances.append(dis_min)
                periodReached = True
                periodMindistances.append(dis_min)
                periodMaxdistances.append(dis_max)
                #print(ydataHull[0]/(b_two*a_two))
                data_line.append(i)

            elif(math.ceil(math.log2(count)) == math.log2(count) and periodReached == False):
                del possiblePeriodX[:]
                del possiblePeriodY[:]
                
                #possiblePeriodX = list(xdataHull)
                #possiblePeriodX = []

                for k in range(0,len(xdataHull)):
                    possiblePeriodX.append(xdataHull[k])
                    possiblePeriodY.append(ydataHull[k])
                






yData = []      #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xData = []          # -1 if point is in hull, x value instead
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
gradients = []      #gradients between the hullpoints
possiblePeriodX = []
possiblePeriodY = []


#a_one | a_two | b_one | b_two | g_one | g_two | StepsToVerticalPeriod | StepsToNewVerticalPeriod
data_line = []      #line which gets written in CSV

# PARABOLA COEFFICIENTS
a_one = 1            #a_one , a_two , b_one and b_two are the Nenner(two) and Zaehler(one) from f(x) = ax^2 + bx
a_two = 44
b_one = 1
b_two = 50         # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 1

#THEORETICALSTUFF
highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
if(highestx<100):
    highestx = 100
numPeelings = 1
periodReached  = False


#VIEWSTUFF
printstep = 0      #printstep == 1 -> jeder Schritt wird geprintet
plot = 0          #plot ==1 -> Graphen werden geplottet
plotPeriod = 0      #plotPeriod == 1 -> nur Graphen mit xdata[0] == 0 werden geplottet

#toinvestigate = [2,8,22,44]
#toinvestigate = [2,8,22,44,86,128]

#toinvestigate = [1,4,11,22,43,64,107,150,211,274,385,462,619,748,895,1066,1339,1522,1865,2096,2397,2730,3237]
#toinvestigate = [748,895,1066,1339,1522,1865,2096,2397,2730,3237]

#toinvestigate = [5,22,44,50,88,110,132,154,176,500]
#toinvestigate = [2,3,4]
toinvestigate = [15]
path = f"../Investigate Specific/All Data b=0/"

os.mkdir(path)

globalWriter,file = csvStuff.createWriter(path+"LogAll.csv")
header = ["a_one","a_two","b_one","b_two","g_one","g_two","steps til first","steps til second period","horizontal Period","average time in ms","Average Vertical Translation","Average Tube Thickness", "Minimal Tube Thickness", "Maximal Tube Thickness","Average Tube Thickness in Period","Average Vertical Translation in Period", "Max Tube Thickness in Period"]
globalWriter.writerow(header)

allDistances = []

g_two = 1
os.mkdir(path+"Logs")
newTime =  time.time()
for x in toinvestigate:
    for j in range(1,101,1):
        for i in range(j,101,1):
            for l in range(0,11,11):
                for m in range(1,11,11):

                    a_one = j
                    a_two = i
                    b_one = l

                    b_two = m
                    if(b_one == 0 and abs(b_two)!=1):
                        continue
                    

                    highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
                    if(highestx<50):
                        highestx=50
                    if(calc.ggT(a_one,a_two)!=1):
                        continue
                    if(calc.ggT(b_one,b_two)!=1):
                        continue
                    #gGt = calc.ggT(abs(b_one),abs(b_two))
                    #b_one = int(b_one/gGt)
                    #b_two = int(b_two/gGt)
                    name = path+"Logs/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)
                    print(name)
                    
                    os.mkdir(name)
                    distanceWriter,distanceFile = csvStuff.createWriter(name+"/Distances.csv")
                    headerDis = ["x_min","dis_min","x_max","dis_max"]
                    distanceWriter.writerow(headerDis)                    
                    #debugWriterX,fileX = csvStuff.createWriter(name+"/xValues.csv")
                    #debugWriterY,fileY = csvStuff.createWriter(name+"/yValues.csv")
                    #debugWriterDis,fileDis = csvStuff.createWriter(name+"/debuggerVerticalDis.csv")
                    debugWriterCorners,fileCorner = csvStuff.createWriter(name+"/Corners.csv")
                    #debugWriterGrad,fileDif = csvStuff.createWriter(name+"/debbugerGrad.csv")
                    #vectorWriter,vecFile = csvStuff.createWriter(name+"/vectors.csv")

                    mainTwo(highestx,numPeelings, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)
                    timeNeeded = time.time()-newTime
                    print(timeNeeded)
                    
                    #fileX.close()
                    #fileY.close()
                    distanceFile.close()
                    #fileDis.close()
                    fileCorner.close()
                    #fileDif.close()

