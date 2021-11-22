from numpy.lib.function_base import diff
import calc
from random import *
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import operator


# receives the calculated corners of the convex hull (xHull,yHull) and the distances inbetween the
#
# periodDistances is the array that stores all the distance-lengths in one horizontal period(which are the distances of the cornerpoints from [H,2H])
# this function continues this distances from startIndex to endIndex i.e. corrects the convex hull of the parabola
# in the interall [startIndex,endIndex]
#
# xHull,yHull are the current x and y-values of the cornerpoints of the CH, distances are the horizontal distances
# in between them
# yAll[i] is the next possible y-values of the xValue i
#
# returns updated CH (xHull,yHull) and the horizontal distances inbetween them
#
def correctRightSide(startIndex,endIndex, xHull, yHull, distances, periodDistances,yAll,xAll):
    index = 0 # see where we are in periodDistances
    for i in range(startIndex,endIndex):
        distances[i]=periodDistances[index] # correct distance
        xHull[i+1]=xHull[i]+distances[i]    # correct x-value
        if(xHull[i+1] in xAll):
            elementindex = xAll.index(xHull[i+1])   #index of corresponding x-value
            yHull[i+1] = yAll[elementindex]         #correct y-value
            index+=1
            if(index==len(periodDistances)):        # we reached end of periodDistances and start from beginning
                index = 0
        else:   # corresponding yValue is not in calculated area
            for j in range(i, len(distances)): # remove current point and all points from hull which are more right than the current one
                del(distances[len(distances)-1])
                del(xHull[len(xHull)-1])
                del(yHull[len(yHull)-1])
            return xHull, yHull, distances
    return xHull, yHull, distances



# same as the function correctRightSide, just that it starts at leftStartIndex and goes down 0
def correctLeftSide(leftStartIndex, periodDistances, xHull, yHull, distances,yAll,xAll):
    index = len(periodDistances)-1
    for i in range(leftStartIndex,-1,-1):
        if(xHull[i+1]-periodDistances[index]>=xAll[0]): # current point is inside calculated area
            distances[i]=periodDistances[index]
            xHull[i]=xHull[i+1]-distances[i]
            elementindex = xAll.index(xHull[i])
            yHull[i] = yAll[elementindex]
            index-=1
            if(index==-1):
                index = len(periodDistances)-1
        else: # corresponding yValue is not in calculated area
            j=0
            while(j < i+1): # remove all points from hull which are more left than the current one and current point
                
                del(xHull[0])
                del(yHull[0])
                del(distances[0])
                j+=1
            return xHull, yHull, distances
    return xHull, yHull, distances



# receive the xValues of a CH, xHull and returns the array corners with:
#   corners[i] == 1 iff (i,y) is in CH
def correctCorners(corners, xHull,xAll):
    for i in range(0,len(corners)):
        corners[i]=0
    for i in range(0,len(xHull)):
        elementindex = xAll.index(xHull[i])
        corners[elementindex]=1 
    return corners



# receives a CH (xHull,yHull) and continues the horizontal distances from [H,2H] further to
# the right with "correctRightSide"
# the left with "correctLeftSide"
#
# if writeAlllogs == True the changes will get written to Logfiles 
def correctHull(xHull,yHull,corners,distances,yData,xData):
    start = int(len(distances)/3)
    periodDistances = calc.getPeriodDistances(start,len(distances),a_two,distances)  # collect the horizontal distances which are inbetween [H/2,1.5H]

    if(periodDistances == -1):
        print("problem")
        return -1
    xHull, yHull, distances = correctRightSide(start+len(periodDistances),len(distances),xHull, yHull, distances, periodDistances,yData,xData) #correct [0,0.5H]
    xHull, yHull, distances = correctLeftSide(start-1,periodDistances,xHull, yHull, distances,yData,xData) #correct [1.5H,2H]
    corners = correctCorners(corners, xHull,xData) # update 01-sequence
    return xHull,yHull,corners,distances


#create the vectors (x,y) with, 0<x<=y<=n
#and for each (x,y) take the smallest vectors v in Z2 with n*v=(x,y)
#store x and y value and gradient of v in "output"
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
                toInvestigateX.append(j/ggt)    # get x-value of v
                toInvestigateY.append(i/ggt)    # get y-value of v
                grad.append(i/float(j))         # get gradient of v
                output.append([j/ggt,i/ggt,i/float(j)]) #output[i] = [x,y,grad}
    return toInvestigateX,toInvestigateY,grad,output

#turns vectors to  x,y-values 
def getGraph(allList):
    halfX= [0]
    halfY= [0]
    for i in range(1,len(allList)): #create data set
        halfX.append(allList[i][0]+halfX[-1])
        halfY.append(allList[i][1]+halfY[-1])
    x = []
    y = []

    for i in range(len(halfX)-1,0,-1): #[-k,0]
        x.append(halfX[i]*-1)
        y.append(halfY[i])
    for i in range(0,len(halfX)): #[0,k]
        x.append(halfX[i])
        y.append(halfY[i])
    return x,y


# gets points (plotX[i],plotY[i]) and finds fills xData with all integer values
# in between plotX[0] and plotX[-1] 
# yData[i] i corresponding y-Value of xData[i], s.t. (yData[i],xData[i]) is in or above
# convex hull of (plotX,plotY)

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



#corners is an array, which saves, if an element from yData is in the hull
#corners[i] == 1 -> ith element from yData is in the hull
#corners[i] == 0 -> ith element from yData is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull
#xData a
#

def initialize(n):
    global corners,yData,xdataHull,ydataHull,distances,possiblePeriodX,possiblePeriodY,xData

    xData = []          # -1 if point is in hull, x value instead
    yData = []          #represents the set of points of which the hull gets calculated
    corners = []        #saves if a point of the set is in the hull
    xdataHull = []      #x values of the points which are in the hull
    ydataHull = []      #y values of the points which are in the hull
    distances = []      #distances between the hullpoints of the current hull
    possiblePeriodX = []#termination parabola, to check if a CH is a translation of another
    possiblePeriodY = []


    x,y,grad,all = getStartingParabola(n) #all[i]=  [x,y,grad] with 0<y<=x<=n and (x,y) in Z2
    s = sorted(all, key = operator.itemgetter(2)) #sort all ascending by gradient
    plotX,plotY = getGraph(s)   #turns vectors to  x,y-values in intevall [-k,k], where k=s[-1][0]
    xData,yData = getAllData(plotX,plotY) #fill xData and yData with all the points, which are on or above the CH

    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,len(xData)):
        corners.append(1)

    xdataHull,ydataHull = calc.make_para_convex(xData,yData)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData,xData)
    for i in range(0,len(xdataHull)):
        possiblePeriodX.append(xdataHull[i])
        possiblePeriodY.append(ydataHull[i])




# makes one step of the gridPeeling and updates the hull values
# (xData[i],yData[i])  is the i-th gridvertex, which is inside the CH
# (xdataHull[i],ydataHull[i]) is the i-the corner of the CH
# distances[i] is the horizontal distance between the i-th and i+1-th corner of the CH
# corners[i] == 0 iff (xData[i],yData[i]) is in CH, 1 else
def oneStep():
    global corners,yData,xdataHull,ydataHull,distances,xData
    xdataHull = []
    ydataHull = []

    # if a point (xData[i],yData[i]) is in the CH, the next possible Point with x=xData[i] has the
    # y-Value one gridlength above the current y-Value, wich is yData[i]+gridlength
    for i in range (0,len(corners)):
        if corners[i]==1:
            yData[i] = yData[i]+ 1
        corners[i]=1    #will get updated later anyway

    xdataHull,ydataHull = calc.make_para_convex(xData,yData) # make the hull convex by removing the "inner" points
    distances = calc.calc_distances_one(xdataHull) # update the horizontal distances
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData,xData) # correct the mistakes mistakes at the edge



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



def mainTwo(numX,a_two_in):
    global a_two

    periodReached = False
    a_two = a_two_in
    n = numX
    
    #initialize the plot stuff with a grid
    fig,ax=plt.subplots()
    ax.set_xticklabels([])    
    locx = plticker.MultipleLocator(base=1)
    locy = plticker.MultipleLocator(base=1)
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.grid(b= True, which='both', axis='both', linestyle='-',zorder =10)
    

    initialize(n)
    plt.scatter(xdataHull,ydataHull)
    plt.plot(xdataHull,ydataHull)
    
    vertical_Period=0
    while(True):
        oneStep() #perform one peeling
        if(periodReached==True):
            vertical_Period+=1
        plt.scatter(xdataHull,ydataHull)
        plt.plot(xdataHull,ydataHull)       
        if(xdataHull==possiblePeriodX and testPeriod(ydataHull,possiblePeriodY)): #CH is vertical translation of another one
            if(periodReached == True):
                print("time period=", vertical_Period)
                break
            periodReached = True

    mostrightx = int(xdataHull[-1])
    leftrightx = int(xdataHull[0])

    x = np.linspace(leftrightx,mostrightx,1000)
    y = (x**2)/(2*a_two)
    plt.plot(x,y,color = '0')
    
    plt.show()





yData = []      #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xData = []          # -1 if point is in hull, x value instead
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
possiblePeriodX = []
possiblePeriodY = []


# necessary stuff 
a_two = 1            #a_one , a_two , b_one and b_two are the Nenner(two) and Zaehler(one) from f(x) = ax^2 + bx
periodReached  = False


###########################################################################
##                                                                       ##
##      this programm displays the grid peeling of vector parabolas      ##
##                                                                       ##
###########################################################################

###############################
##                           ##
##           t - (t+1)       ##
##  1/(2a)    |  Übergang |  ## 
## -------------------       ##
## 1/2   ->  1-2             ##
## 1/8   ->  2-3             ##
## 1/22  ->  3-4             ##
## 1/44  ->  4-5             ##
## 1/86  ->  5-6             ##
## 1/128 ->  6-7             ##  
## 1/214 ->  7-8             ##
## 1/300 ->  8-9             ##
## 1/422 ->  9-10            ##
## 1/548 -> 10-11            ##
## 1/770 -> 11-12            ##
## 1/924 -> 12-13            ##
##                           ##
###############################


# to make it work you you need to take an value a from the table
# and and an corresponding even(!) t. t needs to be even!
# set a and t with this value. You will get the Grid Peeling displayed
# and the number of Peelings it took, till the first Approximation repeated
# itself, will be printed out!

a = 64
t = 6

mainTwo(    t    ,  a )


