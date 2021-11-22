import math
import os
import time
from random import *

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from numpy.lib.function_base import average, diff

import calc
import calcVerticalDis
import csvStuff

# first transforms the grid by stretching it to the standard grid
# then calculates the stretched a_one/a_two and calculates the period
#
# calculates the horizontal Period of the parabola a_one/a_two x^2 + b_one/b_two * x in the grid with length g_one/g_two
# and stretches it by the factor g_two*a_two*b_two to fit it to the space
#
def calculatePeriod():
    global a_one,a_two,b_one,b_two,g_one,g_two  # parabola coefficients and grid variables

    if b_one == 0:                              # case that there is no linear part in the parabola function
        a_one_stretched = a_one * g_one         # stretch parabola to standard grid
        a_two_stretched = a_two * g_two         # stretch parabola to standard grid

        #
        # if a_two_stretched mod 4 =0, then the horizontal period is a_two_stretched/2
        # else it is a_two_stretched
        # since the whole space gets stretched by g_two*a_two*b_two, the horizontal period must be too
        #
        a_one_stretched, a_two_stretched = calc.bruchKuerzen(a_one_stretched,a_two_stretched) #cancel out a
        if(a_two_stretched%4 == 0):
            a_two_stretched = a_two_stretched*g_two*a_two*b_two
            return a_two_stretched/2
        else:
            a_two_stretched = a_two_stretched*g_two*a_two*b_two
            return a_two_stretched
    else:                                     # case that the linear part of the parabolic function !=0
        a_one_stretched = a_one * g_one
        a_two_stretched = a_two * g_two
        a_one_stretched, a_two_stretched = calc.bruchKuerzen(a_one_stretched,a_two_stretched)

        b_one_stretched, b_two_stretched = calc.bruchKuerzen(b_one,b_two)
        periodCase = getPeriodCase(a_two_stretched,b_two_stretched) # the horizontal period is dependent on a_two and b_two. There exist different cases, which get returned here

        if(periodCase==0):  # catch possible mistake
            print("Problem")
            return

        period = getPeriod(periodCase,a_two_stretched,b_two_stretched) # returns the unstretched Period for the chosen a_two and b_two
        period_stretched =period*g_two*a_two*b_two  # since the whole space gets stretched by g_two*g_two*a_two*b_two, the horizontal period must be too (it is already stretched by g_two)
        return period_stretched

#
# calculates the horizontal Period of the parabola a_one/a x^2 + b_one/b * x in Z2
# a_one/a and b_one/b need to be fully cancelled down
#
def getHorizontalPeriod(a,b):
    periodCase = getPeriodCase(a,b)
    return getPeriod(periodCase,a,b)



#
# calculates the horizontal Period of the parabola a_one/a x^2 + b_one/b * x in Z2
# a_one/a and b_one/b need to be fully cancelled down
#
# there are 5 different cases (to be completely correct just 3) a-e:
#   a : period = ab/gcd(a,b)
#   b : period = ab/2gcd(a/2,b)
#   c : period = ab/gcd(a,b)
#   d : period = ab/gcd(a,b)
#   e : period = ab/2gcd(a,b)

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
    return period

# there are 5 different cases (to be completely correct just 3) a-e which can be differentiated to
# calculate the horizontal period of the parabola a_one/a x^2 + b_one/b * x in Z2
#   a : a mod 2 !=0
#   b : a mod 4 ==0
#   c : a mod 2==0 And a mod 4 !=0 And b mod 2 != 0
#   d : a mod 2==0 And a mod 4!=0 And b mod 4 == 0
#   e : a mod 2==0 And a mod 4!=0 And b mod 2 == 0 And b mod 4 != 0

def getPeriodCase(a, b):
    if (a % 2 != 0):
        return 'a'
    if (a % 4 == 0):
        return 'b'
    if (a % 2 == 0 and a % 4 != 0 and b % 2 != 0):
        return 'c'
    if (a % 2 == 0 and a % 4 != 0 and b % 4 == 0):
        return 'd'
    if (a % 2 == 0 and a % 4 != 0 and b % 2 == 0 and b % 4 != 0):
        return 'e'
    return 0

#
# to make everything integers the whole space gets stretched with
# g_two*g_two*a_two
# this means the whole space gets multiplied with the matrix
#
# |g_two*g_two*a_two*b_two             0         |
# |       0               g_two*g_two*a_two*b_two|
#
#
# input represents the x-value of the possible hull-values
# it is a natural number between 0 and n, where n is 3*horizontal period
# therefore it represents x = input *g_1/g_2 in the grid with length g_1/g_2
# it gets stretched by g_two*g_two*a_two*b_two
#
# Summary:
# f(x) = a_one/a_two * x^2 + b_one/b_two *x
# grid = g_one/g_two
# x -> x * g_two * g_two * a_two * b_two
# x = input * g_one/g_two
# x -> input * g_one * g_two *a_two *b_two
def transformNormalToInt(input):
    return a_two*b_two * g_two*g_one*input



# returns the stretched grid length
#
# grid -> grid * g_two * g_two * a_two *b_two
# grid = g_one/g_two
# grid -> g_one * g_two * a_two * b_two
def getGrid():
    return g_one*g_two*a_two * b_two


# returns the real grid length
def getRealGrid():
    return g_one/float(g_two)

# returns f(x) but stretched and fitted to the grid
# f(x) =  a_one/a_two *(input * g_one/g_two)^2 + b_one/b_two * (input * g_one/g_two)
# f(x) -> a_one/a_two *(input * g_one/g_two)^2 *g_two *g_two *a_two * b_two +  b_one/b_two * (input * g_one/g_two) *g_two *g_two *a_two * b_two
# = a_one * b_two * input^2 *g_one^2 + b_one * input * g_one * g_two * a_two
#
# 1. case: f(x) = n*grid -> liegt auf dem grid und muss nicht "nach oben" angepasst werden
#
# 2. case: n*grid < f(x) < n+1 * grid
#
# mod = f(x) - n*grid -> f(x) - mod = n*grid
# -> f(x) - mod + grid = n+1 * grid

def parabola_func(input):
    mod = (input* input*a_one*b_two *g_one*g_one + input * a_two * b_one * g_one * g_two)%getGrid()
    if(mod == 0):
        return input* input*a_one*b_two *g_one*g_one + input * a_two * b_one * g_one * g_two
    else:
        return input* input*a_one*b_two *g_one*g_one + input * a_two * b_one * g_one * g_two + getGrid()-mod




# receives an ordered set of points, where xdata and ydata are the x- and y-Values of the points
#
#  calculates and returns bottom convex hull
# Algorithm taken from : https://mycampus.imp.fu-berlin.de/access/content/group/e01596a9-96d7-4004-9a5b-ce451671435e/Folien/Geometrie.pdf
#
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
            while(l>=1 and gradOne >= gradTwo): # check if righTurn or straith line and if so, remove the point from the set
                xdataHull.pop()
                ydataHull.pop()
                l -= 1
                if(l>=1):
                    gradOne = (ydataHull[l]-ydataHull[l-1]) * (xdata[k]-xdataHull[l])
                    gradTwo = (ydata[k]-ydataHull[l]) * (xdataHull[l]-xdataHull[l-1])
        l += 1
        xdataHull.append(xdata[k])  # append next possible value to convex hull
        ydataHull.append(ydata[k])
    return xdataHull,ydataHull



# receives the calculated corners of the convex hull (xHull,yHull) and the distances inbetween the
#
# periodDistances is the array that stores all the distance-lengths in one horizontal period(which are the distances of the cornerpoints from [H,2H])
# this function continues this distances from startIndex to endIndex i.e. corrects the convex hull of the parabola
# in the interall [startIndex,endIndex]
#
# xHull,yHull are the current x and y-values of the cornerpoints of the CH, distances are the horizontal distances
# in between them
# yAll[i] is the next possible y-values of the xValue i*g_1/g_2
#
# returns updated CH (xHull,yHull) and the horizontal distances inbetween them
#
def correctRightSide(startIndex,endIndex, xHull, yHull, distances, periodDistances,yAll):
    index = 0   # see where we are in periodDistances
    for i in range(startIndex,endIndex):
        distances[i]=periodDistances[index] # correct distance
        xHull[i+1]=xHull[i]+distances[i]    # correct xValue
        elementindex = int(round(xHull[i+1]/(a_two*g_two*g_one*b_two),0))   #find index of corresponding yValue

        if(elementindex<len(yAll)): # corresponding yValue is in calculated area
            yHull[i+1] = yAll[elementindex] # update yValue
            index+=1
            if(index==len(periodDistances)): # we reached end of periodDistances and start from beginning
                index = 0
        else:   # corresponding yValue is not in calculated area
            for j in range(i, len(distances)): # remove current point and all points from hull which are more right than the current one
                del(distances[len(distances)-1])
                del(xHull[len(xHull)-1])
                del(yHull[len(yHull)-1])
            return xHull, yHull, distances
    return xHull, yHull, distances

# same as the function correctRightSide, just that it starts at leftStartIndex and goes down 0
def correctLeftSide(leftStartIndex, periodDistances, xHull, yHull, distances,yAll):
    index = len(periodDistances)-1
    for i in range(leftStartIndex,-1,-1):
        if(xHull[i+1]-periodDistances[index]>=0):   # current point is inside calculated area
            distances[i]=periodDistances[index]     # update distances
            xHull[i]=xHull[i+1]-distances[i]        # updates xValue
            elementindex = int(round(xHull[i]/(a_two*g_two*g_one*b_two),0))
            yHull[i] = yAll[elementindex]       #updates yValue
            index-=1
            if(index==-1):
                index = len(periodDistances)-1 # we reached start of periodDistances and start from end
        else:   # corresponding yValue is not in calculated area
            j=0
            while(j < i+1): # remove all points from hull which are more left than the current one and current point

                del(xHull[0])
                del(yHull[0])
                del(distances[0])
                j+=1
            return xHull, yHull, distances
    return xHull, yHull, distances



# receive the xValues of a CH, xHull and returns the array corners with:
#   corners[i] == 1 iff ((i*g_1/g_2),y) is in CH
def correctCorners(corners, xHull):
    for i in range(0,len(corners)):
        corners[i]=0
    for i in range(0,len(xHull)):
        elementindex = int(round(xHull[i]/(a_two*g_two*g_one*b_two),0)) # stretch xHull[i] back to Z2
        corners[elementindex]=1
    return corners



# receives a CH (xHull,yHull) and continues the horizontal distances from [H,2H] further to
# the right with "correctRightSide"
# the left with "correctLeftSide"
#
# if writeAlllogs == True the changes will get written to Logfiles 

def correctHull(xHull,yHull,corners,distances,yData,writeAllLogs):


    if(writeAllLogs==True): #write CSV's of values before correction
        csvStuff.writePeeling(debugWriterX,"vorher","xHull",xHull)
        csvStuff.writePeeling(debugWriterY,"vorher","yHull",yHull)
        csvStuff.writePeeling(debugWriterCorners,"vorher","Corners",corners)
        csvStuff.writePeeling(debugWriterDis,"vorher","dis",distances)


    start = int(len(distances)/3)
    periodDistances = calc.getPeriodDistances(start,len(distances),calculatePeriod(),distances) # collect the horizontal distances which are inbetween [H,2H]

    if(periodDistances == -1): #the distances did not sum up to the horizontal Period
        print("problem")
        return -1

    xHull, yHull, distances = correctRightSide(start+len(periodDistances),len(distances),xHull, yHull, distances, periodDistances,yData) # correct [2H,3H]
    xHull, yHull, distances = correctLeftSide(start-1,periodDistances,xHull, yHull, distances,yData) # correct [0,H]
    corners = correctCorners(corners, xHull) # update 01-sequence

    if(writeAllLogs==True): # write CSV's of values after correction
        csvStuff.writePeeling(debugWriterX,"nachher","xHull",xHull)
        csvStuff.writePeeling(debugWriterY,"nachher","yHull",yHull)
        csvStuff.writePeeling(debugWriterCorners,"nachher","Corners",corners)
        csvStuff.writePeeling(debugWriterDis,"nachher","dis",distances)
    return xHull,yHull,corners,distances


# fills the array yData with f(x) rounded up to the grid
# f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize}
# corners is an array, which saves, if an element from yData is in the hull
# corners[i] == 1 -> ith element from yData is in the hull
# corners[i] == 0 -> ith element from yData is not in the hull
# xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(size,writeLogs):

    # (xData[i],yData[i])  is the i-th gridvertex, which is inside the CH
    # (xdataHull[i],ydataHull[i]) is the i-the corner of the CH
    # distances[i] is the horizontal distance between the i-th and i+1-th corner of the CH
    # corners[i] == 0 iff (xData[i],yData[i]) is in CH, 1 else
    # (possiblePeriodX[i],possiblePeriodY[i]) is the i-th corner of the termination CH
    global corners,yData,xdataHull,ydataHull,distances,possiblePeriodX,possiblePeriodY,xData





    xData = []          # -1 if point is in hull, x value instead
    yData = []          #represents the set of points of which the hull gets calculated
    corners = []        #saves if a point of the set is in the hull
    xdataHull = []      #x values of the points which are in the hull
    ydataHull = []      #y values of the points which are in the hull
    distances = []      #distances between the hullpoints of the current hull
    possiblePeriodX = []#termination parabola, to check if a CH is a translation of another
    possiblePeriodY = []

    # calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        corners.append(1)
        xData.append(transformNormalToInt(i))
        yData.append(parabola_func(i))


    xdataHull,ydataHull = make_para_convex(xData,yData)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)  #collect horizontal distances between Corners of CH
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData,writeLogs) #correct the CH
    
    for i in range(0,len(xdataHull)):   #initialize possible termination condidition
        possiblePeriodX.append(xdataHull[i])
        possiblePeriodY.append(ydataHull[i])


# returns the array averageTranslation which contains the the differences between the values
# in MinVerticalDis
# since MinVertical is the Translation of ax^2+bx till it reached the current CH, the difference in
# these distances can be seen as the Translation of a peeling

def getAverageVerticalTranslation(MinVerticalDis):
    averageTranslation = []
    for i in range(1,len(MinVerticalDis)):
        averageTranslation.append(MinVerticalDis[i]-MinVerticalDis[i-1])
    return averageTranslation


# makes one step of the gridPeeling and updates the hull values
def oneStep():

    #(xData[i],yData[i])  is the i-th gridvertex, which is inside the CH
    #(xdataHull[i],ydataHull[i]) is the i-the corner of the CH
    #distances[i] is the horizontal distance between the i-th and i+1-th corner of the CH
    #corners[i] == 0 iff (xData[i],yData[i]) is in CH, 1 else
    global corners,yData,xdataHull,ydataHull,distances,xData,writeLogs

    xdataHull = []
    ydataHull = []
    gridVar = getGrid() #length of grid

    #if a point (xData[i],yData[i]) is in the CH, the next possible Point with x=xData[i] has the
    #y-Value one gridlength above the current y-Value, wich is yData[i]+gridlength
    for i in range (0,len(corners)):
        if corners[i]==1:
            yData[i] = yData[i]+ gridVar
        corners[i]=1    #will get updated later anyway


    xdataHull,ydataHull = make_para_convex(xData,yData) # make the hull convex by removing the "inner" points
    distances = calc.calc_distances_one(xdataHull) # update the horizontal distances
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData,writeLogs) # correct the mistakes mistakes at the edge

# check if yData[i] is a vertical translation of possibleY[i] with the same
# translation for all i
def testPeriod(ydata,possibleY):
    difference = ydata[0]-possibleY[0]
    for i in range(0,len(ydata)):
        if(possibleY[i]+difference != ydata[i]):
            print(difference)
            print(possibleY[i]-ydata[i])
            return False
    return True

#
#calculate grid peeling for: f(x) = a_one_in/a_two_in * x^2 + b_one_in/b_two_in *x in the grid with grid length g_one_in,g_two_in
#
def main(numX,a_one_in,a_two_in, b_one_in, b_two_in , g_one_in,g_two_in,writeLogs_in):
    count = 0


    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances,a_one,a_two,b_one, b_two,g_one,g_two, data_line,possiblePeriodX,possiblePeriodY,writeLogs
    a_one,a_two,b_one,b_two,g_one,g_two = a_one_in,a_two_in,b_one_in, b_two_in,g_one_in,g_two_in
    highestx = numX
    writeLogs = writeLogs_in #if True for there will be files, to examine the different peelings
    
    del data_line[:]        #the row which gets written in the "Summary"-Log
    data_line.append(a_one)
    data_line.append(a_two)
    data_line.append(b_one)
    data_line.append(b_two)
    data_line.append(g_one)
    data_line.append(g_two)


    initialize(highestx,writeLogs) #calculate the first approximation of the parabola

    periodReached = False  #there was a CH which was a vertical translation of possiblePeriod[]
    periodMaxdistances = []  # contains the thickness of the tube in which the approximation is for each peeling in the time-period
    periodMindistances = []  # contains the minimum distance from the parabola ax^2+bx to the approximation for each peeling in the time period
    times = [] # contains the seconds it took to do the i-th peeling

    i=0
    while(True):
        i = i+1
        timeStart = time.time()
        oneStep()       # make one peeling
        timeEnd = time.time()
        timeDiff = timeEnd-timeStart
        times.append(timeDiff)

        x_max,dis_max = calcVerticalDis.getMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull) #dis_max =maximum distance from ax^2+bx to parabola , x_max = x-value where the maximum distance is
        x_min, dis_min = calcVerticalDis.getMinDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull) #dis_min =minimum distance from ax^2+bx to parabola , x_min = x-value where the minimum distance is
        dis_max = dis_max-dis_min   #tube thickness

        if(periodReached==True):
            periodMindistances.append(dis_min)
            periodMaxdistances.append(dis_max)

        if(xdataHull[0]==0):    #possible vertical translation
            count = count+1
            if(xdataHull==possiblePeriodX and testPeriod(ydataHull,possiblePeriodY)): # CH is is vertical translation of (possiblePeriodX,possiblePeriodY)
                if(periodReached == True):  #you reach a translation the second time
                    data_line.append(i-data_line[len(data_line)-1])     #time-period
                    data_line.append(getHorizontalPeriod(a_two,b_two))  #horizontal-period
                    timeAverage = sum(times)/len(times)                 #average time per peeling
                    data_line.append(timeAverage)       

                    AllperiodVerticalTranslation = getAverageVerticalTranslation(periodMindistances)    #get the vertical translations in a time-period

                    periodVerticalTranslation =sum(AllperiodVerticalTranslation)/len(AllperiodVerticalTranslation) #calculate average of vertical translation in a time-period
                    maxTubeThicknessPeriod =  max(periodMaxdistances)   #maximum thickness of tube of all Peelings in time-period
                    averageTubeThicknessPeriod = sum(periodMaxdistances)/(len(periodMaxdistances)) #average thickness of tube of all Peelings in time-period

                    data_line.append(averageTubeThicknessPeriod)
                    data_line.append(periodVerticalTranslation)
                    data_line.append(maxTubeThicknessPeriod)
                    globalWriter.writerow(data_line)

                    break

                periodReached = True
                periodMindistances.append(dis_min)
                periodMaxdistances.append(dis_max)
                data_line.append(i)

            elif(math.ceil(math.log2(count)) == math.log2(count) and periodReached == False):   #initialize new possiblePeriod as termination
                del possiblePeriodX[:]
                del possiblePeriodY[:]
                for k in range(0,len(xdataHull)):
                    possiblePeriodX.append(xdataHull[k])
                    possiblePeriodY.append(ydataHull[k])



################################################################
##                                                            ##
##   here happens some initialization ! (no need to touch)    ##
##                                                            ##
################################################################


#
#global Variables - no need to change
#
yData = []          #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xData = []          # -1 if point is in hull, x value instead
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
gradients = []      #gradients between the hullpoints
possiblePeriodX = []
possiblePeriodY = []


#a_one | a_two | b_one | b_two | g_one | g_two | StepsToVerticalPeriod | StepsToNewVerticalPeriod
data_line = []      #line which gets written in Summary CSV



# PARABOLA COEFFICIENTS
a_one = 1            #a_one , a_two , b_one and b_two are the Nenner(two) and Zaehler(one) from f(x) = ax^2 + bx
a_two = 1
b_one = 0
b_two = 1           # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 1

#THEORETICALSTUFF
highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
if(highestx<50):
    highestx = 50

periodReached  = False


####################################################################
##                                                                ##
##      SET THE VARIABLES "path" and "writeLogs"  AS YOU LIKE     ##
##                                                                ##
####################################################################



path = f"../Test Grenzen/"  #name of directory where all the logs of the peelings and the summary log will be saved
writeLogs = False       #if=="True": for every investigated parabola there will be a folder with Logs for every Peeling, if=="False": no Folder afterwards for every Parabola 



####################################################################


os.mkdir(path)
globalWriter,file = csvStuff.createWriter(path+"Summary.csv") #create the CSV file in which the results will get written and the Object to write in it
header = ["a_1","a_2","b_1","b_2","g_1","g_2","steps til period gets recognized","time period","horizontal period","average time in seconds per peeling","average tube thickness in Period","average vertical translation in period", "max tube thickness in period"]
globalWriter.writerow(header)


if(writeLogs==True):    
    os.mkdir(path+"Logs") #create directory for Logs of Peelings

newTime =  time.time()
toinvestigate = [2,8,22,44]
for x in toinvestigate:
    for j in range(1,11,11):                #values for a_1
        for i in range(j,11,11):            #values for a_2
            for l in range(0,21,1):        #values for b_1
                for m in range(l,21,1):    #values for b_2

                    a_one = 1       #
                    a_two = x       #parabola coefficients:
                    b_one = l       #f(x) = a_one/a_two*x^2 + b_one/b_two*x
                    b_two = m       #

                    if(b_one == 0 and abs(b_two)!=1):   #to avoid multiple times b=0
                        continue

                    highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*horizontalPeriod]
                    
                    if(highestx<50): #to avoid errors which could occur while correcting the hull, if the hull is too small
                        highestx=50
                    
                    #avoid calculation of same values for a and b
                    if(calc.ggT(a_one,a_two)!=1):
                        continue
                    if(calc.ggT(b_one,b_two)!=1):
                        continue

                    name = path+"Logs/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two) #name of folder in which the Log gets written
                    
                    print(name) #to know where in the programm you are at the moment


                    if(writeLogs== True):   #create Files and Objects to write Logs for every Peeling 
                        os.mkdir(name)
                        debugWriterX,fileX = csvStuff.createWriter(name+"/xValues.csv")
                        debugWriterY,fileY = csvStuff.createWriter(name+"/yValues.csv")
                        debugWriterDis,fileDis = csvStuff.createWriter(name+"/verticalDis.csv")
                        debugWriterCorners,fileCorner = csvStuff.createWriter(name+"/Corners.csv")


                    main(highestx, a_one,a_two, b_one , b_two, g_one,g_two,writeLogs) #start the grid peeling
                    
                    if(writeLogs== True):   #close the opened files
                        fileX.close()
                        fileY.close()
                        fileDis.close()
                        fileCorner.close()

