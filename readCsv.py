import csv
from os import read
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

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
    loc = plticker.MultipleLocator(base=intervals)
    loc.MAXTICKS= 694208142317
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    plt.scatter(xdata,ydata)
    plt.show()


def main():
    for row in logReader:
        row = next(logReader)
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
path = "../All Logs/Logs220621/"
logfilename = path + "LogAll.csv" 
logReader = csvStuff.createReader(logfilename)
next(logReader)



#GLOBAL PLOTSTUFF
xdata = []
ydataFirst = []
ydataSecond = []
gridToInvestigate = 100


main()
plot(xdata,ydataSecond)
