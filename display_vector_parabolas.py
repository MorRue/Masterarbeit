from numpy.lib.function_base import diff
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
import operator

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

#
#umschreiben Ecke vorher
#
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
            #gradOne = math.atan2(ydataHull[l]-ydataHull[l-1],xdataHull[l]-xdataHull[l-1])
            #gradTwo = math.atan2(ydata[k]-ydataHull[l],xdata[k]-xdataHull[l])
            while(l>=1 and gradOne >= gradTwo):
                xdataHull.pop()
                ydataHull.pop()
                l -= 1
                if(l>=1):
                    gradOne = (ydataHull[l]-ydataHull[l-1]) * (xdata[k]-xdataHull[l])
                    gradTwo = (ydata[k]-ydataHull[l]) * (xdataHull[l]-xdataHull[l-1])
                    #gradOne = math.atan2(ydataHull[l]-ydataHull[l-1],xdataHull[l]-xdataHull[l-1])
                    #gradTwo = math.atan2(ydata[k]-ydataHull[l],xdata[k]-xdataHull[l])
        l += 1
        xdataHull.append(xdata[k])
        ydataHull.append(ydata[k])
    return xdataHull,ydataHull


def correctRightSide(startIndex,endIndex, xHull, yHull, distances, periodDistances,yAll,xAll):
    index = 0
    for i in range(startIndex,endIndex):
        #if(distances[i]!=periodDistances[index]):
        distances[i]=periodDistances[index]
        xHull[i+1]=xHull[i]+distances[i]
        if(xHull[i+1] in xAll):
            elementindex = xAll.index(xHull[i+1])

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

def correctLeftSide(leftStartIndex, periodDistances, xHull, yHull, distances,yAll,xAll):
    index = len(periodDistances)-1
    for i in range(leftStartIndex,-1,-1):
        #if(distances[i]!=periodDistances[index]):
        if(xHull[i+1]-periodDistances[index]>=xAll[0]):
            distances[i]=periodDistances[index]
            xHull[i]=xHull[i+1]-distances[i]
            elementindex = xAll.index(xHull[i])
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

def correctCorners(corners, xHull,xAll):
    #gridVar = getGrid()

    for i in range(0,len(corners)):
        corners[i]=0

    for i in range(0,len(xHull)):
        elementindex = xAll.index(xHull[i])
        corners[elementindex]=1
 
    return corners

def correctHull(xHull,yHull,corners,distances,yData,xData):

    start = int(len(distances)/3)
    periodDistances = calc.getPeriodDistances(start,len(distances),a_two,distances)

    if(periodDistances == -1):
        print("problem")
        return -1
    
    xHull, yHull, distances = correctRightSide(start+len(periodDistances),len(distances),xHull, yHull, distances, periodDistances,yData,xData)
    xHull, yHull, distances = correctLeftSide(start-1,periodDistances,xHull, yHull, distances,yData,xData)
    corners = correctCorners(corners, xHull,xData)
    #dif = initializeDif(corners,xHull,yHull)

    return xHull,yHull,corners,distances

def getStartingParabola(n):
    toInvestigateX = [0]
    toInvestigateY = [0]
    grad = []
    output = [[0,0,0]]

    toInvestigateX.append(int(n/2))
    toInvestigateY.append(0)
    grad.append(0)
    output.append([int(n/2),0,0]) #x,y,grad
    for i in range(0,n+1):
        for j in range(abs(i),n+1):
            if(i==0):
                continue
            else:
                ggt = calc.ggT(j,i)
                toInvestigateX.append(j/ggt)
                toInvestigateY.append(i/ggt)
                grad.append(i/float(j))
                output.append([j/ggt,i/ggt,i/float(j)]) #x,y,grad
    return toInvestigateX,toInvestigateY,grad,output

def plotRealParabola(a_two,border):
        mostrightx = border
        leftrightx = -1*border

        x = np.linspace(leftrightx,mostrightx,1000)
        y = (x**2)/a_two
        #x = a_two*x*b_two
        plt.plot(x,y, 'r', color = '0')



def getGraph(allList):
    halfX= [0]
    halfY= [0]
    for i in range(1,len(allList)): #punktmenge erzeugen
        halfX.append(allList[i][0]+halfX[-1])
        halfY.append(allList[i][1]+halfY[-1])
    x = []
    y = []

    for i in range(len(halfX)-1,0,-1):
        x.append(halfX[i]*-1)
        y.append(halfY[i])
    for i in range(0,len(halfX)):
        x.append(halfX[i])
        y.append(halfY[i])
    return x,y



def getAllData(plotX,plotY):
    xData= [0]
    yData= [0]

    rightSideX = plotX[int((len(plotX)-1)/2):len(plotX)]
    rightSideY = plotY[int((len(plotY)-1)/2):len(plotY)]

    #s = [[x,y,grad]]
    for i in range(0,len(rightSideX)-1):
        curX,curY = xData[-1],yData[-1]
        rangeX = int(rightSideX[i+1])-int(rightSideX[i])  #deltaX
        rangeY = int(rightSideY[i+1])-int(rightSideY[i])  #deltaY
        for x in range(1,rangeX+1):
            xData.append(curX+x)
            for y in range(0,rangeY+1):
                if(curY*rangeX + x*rangeY <= (curY+y)*rangeX):
                    yData.append(curY+y)
                    break
    x = []
    y = []

    for i in range(len(xData)-1,0,-1):
        x.append(xData[i]*-1)
        y.append(yData[i])
    for i in range(0,len(xData)):
        x.append(xData[i])
        y.append(yData[i])
    return x,y


#fills the array yData with f(x) rounded up to the grid
#f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize} 
#corners is an array, which saves, if an element from yData is in the hull
#corners[i] == 1 -> ith element from yData is in the hull
#corners[i] == 0 -> ith element from yData is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(n):
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

    x,y,grad,all = getStartingParabola(n) #all enthält x,y,grad mit 0<y<=x<=t der Input-wert ist dabei t
    s = sorted(all, key = operator.itemgetter(2)) #nach Steigung sortieren

    plotX,plotY = getGraph(s)   #macht vektoren zu x,y-Werten - allerdings auch Werte, die auf einer Strecke liegen!

    xData,yData = getAllData(plotX,plotY)



    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,len(xData)):
        corners.append(1)



    xdataHull,ydataHull = make_para_convex(xData,yData)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData,xData)
    for i in range(0,len(xdataHull)):
        possiblePeriodX.append(xdataHull[i])
        possiblePeriodY.append(ydataHull[i])


#



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
            yData[i] = yData[i]+ 1

        corners[i]=1
 
    
    xdataHull,ydataHull = make_para_convex(xData,yData) #make the hull convex by removing the "inner" points 
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData,xData)


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
    
    del data_line[:]
    data_line.append(a_one)
    data_line.append(a_two)
    data_line.append(b_one)
    data_line.append(b_two)
    data_line.append(g_one)
    data_line.append(g_two)
    
    numsteps = numPeelings       #number of gridpeelings
    n = numX
    


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
    

    initialize(n)
    #print(corners)

    if(plot ==1):
        plt.scatter(xdataHull,ydataHull)

        plt.plot(xdataHull,ydataHull)
    '''
    x_max,dis_max = calcVerticalDis.getMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
    x_min, dis_min = calcVerticalDis.getMinDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
    dis_max = dis_max-dis_min
    dis_all = calcVerticalDis.getAllMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
    line = [a_one,a_two,b_one,b_two,0,x_min,dis_min,x_max,dis_max]
    #print("Peeling",0,": x-Val des min. Abst.:",x_min,", Min. Abst.:",round(dis_min,4),", x-Val des max. Abst.:",x_max,", Max. Abs:",round(dis_max,4))
    #distanceWriter.writerow(line)
    x,y = calc.getBothFromOne(dis_all)
    #plt.plot(x,y)
    #print("initialized")    
    '''
        


    

    #for i in range(1,numsteps):
    
    i=0
    while(True):
        i = i+1
        oneStep()
        #print(xdataHull[len(xdataHull)-1]/a_two/b_two)
        '''
        x_max,dis_max = calcVerticalDis.getMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
        x_min, dis_min = calcVerticalDis.getMinDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
        dis_max = dis_max-dis_min
        line = [a_one,a_two,b_one,b_two,i,x_min,dis_min,x_max,dis_max]


        #dis_all = calcVerticalDis.getAllMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)
        #x,y = calc.getBothFromOne(dis_all)
        #plt.plot(x,y)

        line = [a_one,a_two,b_one,b_two,0,x_min,dis_min,x_max,dis_max]
        #print("Peeling:",0,x_min,dis_min,x_max,dis_max)
        #debugWriterDis.writerow(line)
        #distanceWriter.writerow(line)
        #print("Peeling",i,": x-Val des min. Abst.:",x_min,", Min. Abst.:",round(dis_min,4),", x-Val des max. Abst.:",x_max,", Max. Abs:",dis_max)
        '''
        if(plot ==1):
            plt.scatter(xdataHull,ydataHull)
            plt.plot(xdataHull,ydataHull)       


        if(xdataHull==possiblePeriodX and testPeriod(ydataHull,possiblePeriodY)):
            if(periodReached == True):
                data_line.append(i-data_line[len(data_line)-1])
                print("vertical Period: ",data_line[-1])
                data_line.append(getHorizontalPeriod(a_two,b_two))
                print("-------Period found!--------")
                #data_line.append([x_min,dis_min,x_max,dis_max])
                #
                #Decomment to write Logs
                #                    
                #globalWriter.writerow(data_line)

                break
            periodReached = True
            #print(ydataHull[0]/(b_two*a_two))
            data_line.append(i)
        '''
        elif(math.ceil(math.log2(count)) == math.log2(count) and periodReached == False):
            del possiblePeriodX[:]
            del possiblePeriodY[:]
            
            #possiblePeriodX = list(xdataHull)
            #possiblePeriodX = []

            for k in range(0,len(xdataHull)):
                possiblePeriodX.append(xdataHull[k])
                possiblePeriodY.append(ydataHull[k])
        '''
                
     
    if plot == 1 or plotPeriod==1:
        
        mostrightx = int(xdataHull[-1]/a_two/b_two)
        leftrightx = int(xdataHull[0]/a_two/b_two)

        x = np.linspace(leftrightx,mostrightx,1000)
        y = a_one*(x**2)/a_two + b_one * x /b_two 
        #x = a_two*x*b_two
        plt.plot(x,y, 'r', color = '0')
        
        plt.show()





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
b_one = 0
b_two = 1       # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 1

#THEORETICALSTUFF
highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
if(highestx<50):
    highestx = 50
numPeelings = 0
periodReached  = False


#VIEWSTUFF
printstep = 0      #printstep == 1 -> jeder Schritt wird geprintet
plot = 1         #plot ==1 -> Graphen werden geplottet
plotPeriod = 0      #plotPeriod == 1 -> nur Graphen mit xdata[0] == 0 werden geplottet


#debugWriterX = csvStuff.createWriter("../debuggerX.csv")
#debugWriterY = csvStuff.createWriter("../debuggerY.csv")
#debugWriterDis = csvStuff.createWriter("../debuggerDisAll.csv")



'''
          t - (t+1)
 1/(2a)    |  Übergang |  
-------------------
1/2   ->  1-2      
1/8   ->  2-3     
1/22  ->  3-4     
1/44  ->  4-5             
1/86  ->  5-6              
1/128 ->  6-7                 
1/214 ->  7-8              
1/300 ->  8-9
1/422 ->  9-10
1/548 -> 10-11
1/770
1/924

'''
a = 150
t = 8

mainTwo(    t    ,numPeelings, plot,plotPeriod,a_one,   a    , b_one , b_two, g_one,g_two)

toInvestigate_a = [4 , 22 , 64 , 150 , 274 , 462]
toInvestigate_t = [2 ,  4 ,  6 ,   8 ,  10 ,  12]

for i in range(0,len(toInvestigate_a)):
    a = toInvestigate_a[i]
    t = toInvestigate_t[i]
    