import csv
from os import read
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D


import calc
import csvStuff

def testVerticalPeriod(reader, steps_to_First , steps_to_Second,grid, filename):
    next(reader)
    for i in range(0,2*(steps_to_First)):
        next(reader)
    yValueStartPeriod = int(next(reader)[2])

    for i in range(0,2*steps_to_Second-1):
        next(reader)

    yValueEndPeriod = int(next(reader)[2])
    if(yValueEndPeriod- yValueStartPeriod - grid != 0):
        print("-------------------------")
        print("PROBLEM",filename)
        print("-------------------------")


def testHullCorrection(reader):
    max = 0
    for row in reader:
        tmp =len(row)-len(next(reader))
        if(tmp>max):
            max = tmp
    return max

def plot(xdata,ydata):
    intervals = float(gridToInvestigate/float(10)) #Spacing between each line of the displayed grid -> NOT WORKING WTF
    fig,ax=plt.subplots()
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=1)
    locy.MAXTICKS= 694208142317
    locx = plticker.MultipleLocator(base=0.1)
    locx.MAXTICKS= 694208142317
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    plt.scatter(xdata,ydata)
    plt.show()


def plot3d(xdata,ydata,zdata):
    intervals = float(gridToInvestigate/float(10)) #Spacing between each line of the displayed grid -> NOT WORKING WTF
    fig = plt.figure()
    ax = Axes3D(fig)
    #ax = fig.add_subplot(111, projection='3d')
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=5)
    locy.MAXTICKS= 694208142317
    locx = plticker.MultipleLocator(base=0.1)
    locx.MAXTICKS= 694208142317
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.zaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("b")
    ax.zaxis.set_label_text("Steps")
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    ax.scatter(xdata,zdata,ydata,zdir='z')
    plt.show()
    #ax.show() 

def main():
    for row in logReader:

        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        g_one = int(row[4])
        g_two = int(row[5])
        steps_one = int(row[6])
        steps_two = int(row[7])
        
        #
        #uncomment to plot verticalPeriod results
        #

        if(g_two == gridToInvestigate):
            xdata.append(a_one/float(a_two))
            zdata.append(b_one/float(b_two))
            ydataFirst.append(steps_one)
            ydataSecond.append(steps_two)
        


        #
        #uncomment to find out if there is a vertical period which is bigger than grid
        #
        '''
        grid = calc.getGrid(g_one, g_two, a_two, b_two)
        filename = path + "Logs/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)+"/debuggerY.csv"
        print(filename)
        reader = csvStuff.createReader(filename)
        testVerticalPeriod(reader, steps_one, steps_two, grid, filename)
        '''

        #
        #uncomment to find out what the biggest Correction of the hull is
        #
        '''
        grid = calc.getGrid(g_one, g_two, a_two, b_two)
        filename = path + "Logs/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)+"/debuggerY.csv"
        print(filename)
        reader = csvStuff.createReader(filename)
        max = 0
        tmp = testHullCorrection(reader)
        if(tmp>max):
            max = tmp
        print(max)
        '''


#GLOBAL CSV-READER-STUFF
path = "../All Logs/Logs110821/"
logfilename = path + "LogAll.csv" 
logReader = csvStuff.createReader(logfilename)
next(logReader)



#GLOBAL PLOTSTUFF
xdata = []  #a1/a2
zdata = []  #b1/b2
ydataFirst = []
ydataSecond = []
gridToInvestigate = 10


main()
plot(xdata,ydataSecond)
#plot3d(xdata,ydataSecond,zdata)