from functools import total_ordering

from numpy.lib.type_check import iscomplex
import csvStuff
import calc


import fqs

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

#gibt den Wert von f(x) zurück, wobei f(x) die Funktion der Parabel ist
#f(x) = ax^2 +bx
def f(x,a,b):
    y = a*(x**2)+b*x
    return y

#gibt den Wert von f'(x) zurück, wobei f(x) die Funktion der Parabel ist
#f'(x) = 2ax +b
def fPrime(x,a,b):
    y = 2*a*x + b
    return y

#n(x) ist der normalenvektor der Parabel an der Stelle x
#norm gibt die Länge des normalenvektors zurück


def norm(x,a,b):
    if(2*a*x+b !=0):
        output = math.sqrt(1+(1/(2*a*x + b))**2)
    else:
        output =-1
    return output




#Ableitung von ((2*a*x+b)*(a*x^2-m*x+b*x-c)*sqrt(1/(2*a*x+b)^2+1))/(m*(2*a*x+b)+1)
#von https://www.ableitungsrechner.net

#(16*a^4*m*x^4
# +(-8*a^3*m^2+32*a^3*b*m+12*a^3)*x^3
# +(-12*a^2*b*m^2+(24*a^2*b^2-6*a^2)*m+18*a^2*b)*x^2
# +(-6*a*b^2*m^2+(8*a*b^3-4*a*b)*m-4*a^2*c+8*a*b^2+2*a)*x
# +(-b^3-b)*m^2+(2*a*c+b^4-1)*m-2*a*b*c+b^3+b)

def getKoeff(a,b,m,c):
    four = 16*(a**4)*m
    three = -8*a**3*m**2+32*a**3*b*m+12*a**3
    two = -12*a**2*b*m**2+(24*a**2*b**2-6*a**2)*m+18*a**2*b
    one = -6*a*b**2*m**2+(8*a*b**3-4*a*b)*m-4*a**2*c+8*a*b**2+2*a
    const = (-b**3-b)*(m**2)+(2*a*c+b**4-1)*m-2*a*b*c+b**3+b
    coefficients = [four, three, two , one , const]
    return coefficients


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
        return input*input*a_one*b_two *g_one*g_one + input*a_two *b_one*g_one*g_two
    else:
        return input*input*a_one*b_two *g_one*g_one + input*a_two * b_one * g_one * g_two + getGrid()-mod


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
    
    #csvStuff.writePeeling(debugWriterX,"vorher","xHull",xHull)
    #csvStuff.writePeeling(debugWriterY,"vorher","yHull",yHull)
    #csvStuff.writePeeling(debugWriterDis,"vorher","distances",distances)
    #csvStuff.writePeeling(debugWriterCorners,"vorher","Corners",corners)



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
    
    '''
    debugWriterX.writerow(xHull)
    csvStuff.writePeeling(debugWriterY,"nachher","yHull",yHull)
    debugWriterDis.writerow(distances)
    csvStuff.writePeeling(debugWriterCorners,"nachher","Corners",corners)
    #debugWriterCorners.writerow(corners)
    '''

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

    #calculate the bottom y-value for every x-value and add all points to the hull
    for i in range (0,size):
        corners.append(1)
        xData.append(transformNormalToInt(i))
        yData.append(parabola_func(i))


    xdataHull,ydataHull = make_para_convex(xData,yData)     #make the hull convex by removing the "inner" points,
    distances = calc.calc_distances_one(xdataHull)
    xdataHull,ydataHull,corners,distances = correctHull(xdataHull,ydataHull,corners,distances,yData)

#plots the x and y Values stretched back to the Z2 
#x -> x/(g_two^2 * a_two * b_two)

def plotRealValues(xValues,yValues,dis):
    xPlot = []
    yPlot = []
    for i in range(0,len(xValues)):
        x = xValues[i]/(g_two*g_two*a_two*b_two)
        y = yValues[i]/(g_two*g_two*a_two*b_two)
        xPlot.append(x)
        yPlot.append(y)

    plt.scatter(xPlot[:30],yPlot[:30],s=10)
    plt.plot(xPlot[:30],yPlot[:30])
    

    x = np.linspace(xPlot[0],xPlot[30],500)

    # the function, which is y = x^2 here
    y = (a_one/a_two)*x**2 + (b_one/b_two)*x

    plt.plot(x,y, 'r')




def testVerticality(a,b,x_f,x_g,f,g):
    grad_G = (g-f)/(x_g-x_f)
    grad_N = 1/float(fPrime(x_f,a,b))
    output = abs(grad_G)-abs(grad_N)
    return output


def getMaxDistance(a_one,a_two,b_one,b_two,xVals,yVals):
    max = 0
    x_f = 0
    x_g =0
    f = 0
    g = 0
    for i in range(0,len(xVals)-1):
        #stretch everything back
        x_from= xVals[i]/(a_two*b_two)
        x_to = xVals[i+1]/(a_two*b_two)
        f_x_from = yVals[i]/(a_two*b_two)
        f_x_to = yVals[i+1]/(a_two*b_two)

        distance,x_f_tmp,x_g_tmp,f_x_tmp,g_x_tmp = getDistance(a_one,a_two,b_one,b_two,x_from,x_to,f_x_from,f_x_to)

        if(abs(distance)>max):
            max = abs(distance)
            x_f,x_g,f,g = x_f_tmp,x_g_tmp,f_x_tmp,g_x_tmp
    return max,x_f,x_g,f,g


#t(x) = Abstand von (x,(fx)) zu der geraden G(l) = ml+c 
#t(x) = f'(x)/norm(n(x)) * (mx+c-f(x))/(1-f'(x)*m)
def getAbstand(x,c,m,a,b):
    fPrimeFromX = fPrime(x,a,b)
    fFromX =  f(x,a,b)
    normFromNormalAtX = float(norm(x,a,b))

    if(normFromNormalAtX == -1): #case that normale ist senkrecht
        output = (m*x+c-fFromX)
    else:
        output = (fPrimeFromX*normFromNormalAtX * (fFromX-m*x-c))/(1+fPrimeFromX*m)
    return output


def getDistance(a_one,a_two,b_one,b_two,x_from,x_to,f_x_from,f_x_to):
    #m ist Steigung der Geraden der Hülle
    #c = f_x_to - m * x_to ist y-Achsenabschnitt der Geraden der Hülle

    m = (f_x_to-f_x_from)/(x_to-x_from)
    c = f_x_to - (m*x_to)

    a = a_one/float(a_two)
    b = b_one/float(b_two)

    possibleMaximumsXvals = []
    possibleMaximumsXvals = getPossibleXVals(a_one,a_two,b_one,b_two,m,c)
    
    #in case there is no maximum inbetween you need to investigate the corners
    possibleMaximumsXvals.append(x_from)
    possibleMaximumsXvals.append(x_to)

    #just for testing
    #possibleMaximumsXvals.append((x_from+x_to)/float(2))
    #
    possibleMaximumsDistances = []
    for x in possibleMaximumsXvals:
        distance = getAbstand(x,c,m,a,b)
        possibleMaximumsDistances.append(distance)
    #there exists an extremum inbetween x_from and x_to
    #it is x_extreme
    x_funktion = -1
    maxDis = 0
    for i in range(0,len(possibleMaximumsXvals)):
        if(x_from <= possibleMaximumsXvals[i] and possibleMaximumsXvals[i] <= x_to and possibleMaximumsXvals!=0):
            if(maxDis<abs(possibleMaximumsDistances[i])):
                x_funktion = possibleMaximumsXvals[i]
                maxDis = abs(possibleMaximumsDistances[i])
                t = possibleMaximumsDistances[i]
    f_x_extreme = f(x_funktion,a,b)
    #g_x ist der x-Wert der Geraden, an der der größte Abstand gemessen wurde
    #man berechnet ihn, indem man dem x-Wert auf der Parabel die Distanz/(Länge des Normalenvektors) aufaddiert
    x_gerade = x_funktion + t/norm(x_funktion,a,b)
    g_x_extreme = m*x_gerade + c
    return maxDis,x_funktion,x_gerade,f_x_extreme,g_x_extreme

 
def main(numX,plot,plotPeriod,a_one_in,a_two_in, b_one_in, b_two_in , g_one_in,g_two_in):

    #initialize all the global variables
    global gridparam,gridSize,highestx,numsteps,parabola_param,rounder,distances,a_one,a_two,b_one, b_two,g_one,g_two, data_line
    a_one,a_two,b_one,b_two,g_one,g_two = a_one_in,a_two_in,b_one_in, b_two_in,g_one_in,g_two_in
      
    highestx = numX
    


    #this if-statement shall make a grid, but doesnt work for small gridsizes and looks awful..
    #-> made gridsize 0.1 in vizualization...
    
    if plot == 1 or plotPeriod==1:
        intervals = float(getGrid()) #Spacing between each line of the displayed grid -> NOT WORKING WTF
        #intervals = float(getRealGrid())
        fig,ax=plt.subplots()
        #ax.set_xticklabels([]) 
        #ax.set_yticklabels([])
        locx = plticker.MultipleLocator(base=1)
        locx.MAXTICKS= 694208142317
        locy = plticker.MultipleLocator(base=1)
        locy.MAXTICKS= 694208142317
        ax.xaxis.set_major_locator(locx)
        ax.yaxis.set_major_locator(locy)
        plt.gca().xaxis.grid(True)
        ax.grid(b= True, which='both', axis='both', linestyle='-',zorder =10)
    
    initialize(highestx)
    dis,x_f,x_g,f,g =getMaxDistance(a_one,a_two,b_one,b_two,xdataHull,ydataHull)

    print("Maximaler Abstand :",dis)
    print("x-Wert auf Funktion :",x_f, " Funktionswert an der Stelle :", f)
    print("x-Wert auf Gerade :",x_g, " y-Wert an der Stelle :", g)
    print("Differenz zwischen Normalensteigung an dem x-Wert auf Funktion und Steigung der Verbindung beider Punkte = ")
    print(testVerticality(a_one/float(a_two),b_one/float(b_two),x_f,x_g,f,g))

    if plot == 1:
        plotRealValues(xdataHull,ydataHull,dis)
        plt.plot([x_f,x_g],[f,g])
        
        plt.show()


#roots = fqs.quartic_roots(p)
#where p is an array of polynomial coefficients of the form:
#p[0]*x^4 + p[1]*x^3 + p[2]*x^2 + p[3]*x + p[4] = 0
#and roots is an array of resulting four roots.

def getPossibleXVals(a_one,a_two,b_one,b_two,m,c):
    a = a_one/float(a_two)
    b = b_one/float(b_two)
    coefficients = getKoeff(a,b,m,c)
    roots = fqs.quartic_roots(coefficients)
    roots = roots[0].tolist()
    output = []
    for x in roots:
        if(not np.iscomplex(x)):
            output.append(float(x.real))
    return output









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
a_two = 10
b_one = -1
b_two = 9          # b_two must be unequal 0! and should be equal to 1 if b_one == 0

#GRIDSIZE
g_one = 1           #g_one and g_two define the grid. The grid has the form G = g_one/g_two
g_two = 1

#THEORETICALSTUFF
highestx = int(3*g_two*calculatePeriod()/g_one/b_two/a_two/g_two/g_two)        #number of calculated points [0:3*Period]
if(highestx<100):
    highestx = 100
periodReached  = False


#VIEWSTUFF
printstep = 0      #printstep == 1 -> jeder Schritt wird geprintet
plot = 1           #plot ==1 -> Graphen werden geplottet
plotPeriod = 0      #plotPeriod == 1 -> nur Graphen mit xdata[0] == 0 werden geplottet


#debugWriterX = csvStuff.createWriter("../debuggerX.csv")
#debugWriterY = csvStuff.createWriter("../debuggerY.csv")
#debugWriterDis = csvStuff.createWriter("../debuggerDis.csv")


main(highestx, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)

#print(-4%3)

#cProfile.run('main(highestx,numPeelings,printstep, plot,plotPeriod,a_one,a_two, b_one , b_two, g_one,g_two)')
