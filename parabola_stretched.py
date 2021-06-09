import math
from random import *
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np


def ggT(a,b):
    if (b == 0):
        return a
    else:
        return ggT(b, (a % b))


def bruchKuerzen(a,b):
    div = ggT(a,b)
    a_out = a/div
    b_out = b/div
    return a_out,b_out

#first transforms the grid by stretching it to the standard grid
#the calculates the stretched a_one/a_two and calculates the period

def calculatePeriod():
    global a_one,a_two,b_one,b_two,g_one,g_two
    if b_one == 0:
        a_one_stretched = a_one * g_one
        a_two_stretched = a_two * g_two
        a_one_stretched, a_two_stretched = bruchKuerzen(a_one_stretched,a_two_stretched)
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





#fills the array allPoints with f(x) rounded up to the grid
#f(x) = (x- parabola_param) and x elem {0, 1*gridsize, 2*gridsize, ... , (size-1)*gridsize} 
#corners is an array, which saves, if an element from allPoints is in the hull
#corners[i] == 1 -> ith element from allPoints is in the hull
#corners[i] == 0 -> ith element from allPoints is not in the hull
#xdataHull and ydataHull save the x and y values of the points which are in the hull

def initialize(size):
    global corners,allPoints,xdataHull,ydataHull,distances,initialx

    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        allPoints.append(parabola_func(i))
        corners.append(1)
        xdataHull.append(transformNormalToInt(i))
        ydataHull.append(allPoints[i])   

    xdataHull,ydataHull = make_para_convex(xdataHull,ydataHull)     #make the hull convex by removing the "inner" points,
    for i in range(0,len(xdataHull)):
        initialx.append(xdataHull[i])
    distances = calc_distances_one(xdataHull)
    
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,allPoints)


# makes one step of the gridPeeling and updates the hull values
def oneStep():
    global corners,allPoints,xdataHull,ydataHull,distances

    for i in range (0,len(corners)):
        if corners[i]==1:
            allPoints[i] = allPoints[i]+ getGrid()
        corners[i]=1

    del xdataHull[:]
    del ydataHull[:]

    #add the mostright point of every x-value to the hull
    #pretty much just needed for the x=0 value, but yeah, better safe than sorry...
    for i in range (0,len(corners)-1):
        if allPoints[i] >= allPoints[i+1]:
            corners[i] = 0
        else:
            xdataHull.append(transformNormalToInt(i))
            ydataHull.append(allPoints[i])
    
    xdataHull,ydataHull = make_para_convex(xdataHull,ydataHull) #make the hull convex by removing the "inner" points 
    distances = calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,allPoints)


def calc_distances_one(array):
    output = []
    for i in range(0,len(array)-1):
        output.append((array[i+1]-array[i]))
    return output

def main(numX,numPeelings,printDebug,printPeriod,printstep,plot,plotPeriod,a_one_in,a_two_in, b_one_in, b_two_in , g_one_in,g_two_in):

    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances,a_one,a_two,b_one, b_two,g_one,g_two
    a_one,a_two,b_one,b_two,g_one,g_two = a_one_in,a_two_in,b_one_in, b_two_in,g_one_in,g_two_in

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
    print("---------------------- Initial ----------------------")
    print("xdataHull", xdataHull[:20])
    print("ydataHull", ydataHull[:20])
    print("distances",distances[:20],'\n')
    
    if plot == 1 or plotPeriod ==1:
        #plt.scatter(xdataHull,ydataHull,s=10)
        #plt.plot(xdataHull,ydataHull)
        plt.scatter(xdataHull[:10],ydataHull[:10],s=10)
        plt.plot(xdataHull[:10],ydataHull[:10])
    if printDebug == 1:
        print("Initialized:")
        printstuff()
        print("-------------------------")

    for i in range (0,numsteps):
        oneStep()
        if printstep == 1:
            print("---------------------- Peeling",i+1,"----------------------")
            print("xdataHull", xdataHull[:20])
            print("ydataHull", ydataHull[:20])
            print("distances",distances[:20],'\n')

        if plot == 1:
            plt.scatter(xdataHull[:10],ydataHull[:10],s=10)
            plt.plot(xdataHull[:10],ydataHull[:10])
            #plt.scatter(xdataHull,ydataHull,s=10)
            #plt.plot(xdataHull,ydataHull)

        if(xdataHull[0]==0):
            if printPeriod == 1:
                print("---------------------- Peeling",i+1,"----------------------")
                print("xdataHull", xdataHull[:20])
                print("ydataHull", ydataHull[:20])
                print("distances",distances[:20],'\n')
                #oneStep()
            if plotPeriod == 1:
                plt.scatter(xdataHull[:20],ydataHull[:20],s=10, color = '0')
                plt.plot(xdataHull[:20],ydataHull[:20], color = '0')
     
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
    

def findPeriod(xdata):
    period = calculatePeriod()
    sum = 0
    for i in range(1,len(xdata)):
        sum+=xdata[i]
        print(sum)
        if(sum == period):
            print("i=",i)
            print("Period =",sum)
            print("first",xdata[1:i+1])
            print("second", xdata[i+1:2*i+1])
            print("third", xdata[2*i+1:3*i+1])
            if(xdata[1:i+1]==xdata[i+1:2*i+1] and xdata[1:i+1]== xdata[2*i+1:3*i+1]):
                print("success, Periode =", period/(g_two*g_two*a_two*b_two))
            return

def correctHull(xHull,yHull,corners,distances,yAll):
    period = calculatePeriod()
    periodDistances = []
    sum = 0
    start = int(len(distances)/3)
    for i in range(start,len(distances)):
        sum+=distances[i]
        periodDistances.append(distances[i])
        if(sum == period):
            break
        if(sum>period):
            raise Exception("Problem bei a=",a_one,"/",a_two,"Summe =",sum,"Period=",period)
    
    index = 0
    for i in range(start+len(periodDistances),len(distances)):
        distances[i]=periodDistances[index]
        xHull[i+1]=xHull[i]+distances[i]
        elementindex = int(round(xHull[i+1]/(a_two*g_two*g_one*b_two),0))
        if(elementindex<len(yAll)):
            yHull[i+1] = yAll[elementindex]
            index+=1
            if(index==len(periodDistances)):
                index = 0
        else:
            j=i
            while(j<len(distances)):
                del(distances[j])
                del(xHull[j+1])
                del(yHull[j+1])
                j+=1
            break

    index = len(periodDistances)-1
    for i in range(start-1,0,-1):
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
                del(xHull[j])
                del(yHull[j])
                del(distances[j])
                j+=1
            break

    for i in range(0,len(corners)):
        if(transformNormalToInt(i) in xHull):
            corners[i]=1
        else:
            corners[i]=0
    return xHull,yHull,corners,distances




allPoints = []      #represents the set of points of which the hull gets calculated
corners = []        #saves if a point of the set is in the hull
xdataHull = []      #x values of the points which are in the hull
ydataHull = []      #y values of the points which are in the hull
distances = []      #distances between the hullpoints of the current hull
gradients = []      #gradients between the hullpoints
initialx = []


#a_one | a_two | b_one | b_two | g_one | g_two | # calculatedPoints |Calculated Period | Sum Period | FirstPeriodHorizontalValues | StepsToVerticalPeriod | VerticalPeriodHorizontalValues | StepsToNewVerticalPeriod
data_line = []      #line which gets written in CSV

# PARABOLA COEFFICIENTS
a_one = 2           #a_one , a_two , b_one and b_two are the Nenner(two) and Zaehler(one) from f(x) = ax^2 + bx
a_two = 7
b_one = 0
b_two = 1            # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 100

#THEORETICALSTUFF
highestx = 10000        #number of calculated points [0:3*Period]
numPeelings = 200

#VIEWSTUFF
printDebug = 0      #printDebug ==1 -> Konsolenausdruck fuer Werte
printPeriod = 0     #printPeriod ==1 -> moegliche Periode wird auf Konsole gedruckt
printstep = 0      #printstep == 1 -> jeder Schritt wird geprintet
plot = 0            #plot ==1 -> Graphen werden geplottet
plotPeriod = 1      #plotPeriod == 1 -> nur Graphen mit xdata[0] == 0 werden geplottet

main(highestx,numPeelings,printDebug,printPeriod,printstep, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)
#print(calculatePeriod())
#findPeriod(distances)
