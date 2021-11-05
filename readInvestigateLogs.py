
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D



import math
import calc
import csvStuff

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


def findMaxZeros(array):
    count = 0
    max = 0
    for i in range(0,len(array)):
        if(int(array[i])==0):
            count +=1
            if(count>max):
                max =count
        else:
            count = 0
    return max


#writes logs for all subfolders which contain the steigungsdifferenz between the linearen Teilstücke
def investigateVerticalHullDiff():
    Foldername = "Investigate Pattern"
    pathToLogs = f"../All Logs/{Foldername}/Logs/"
    pathToLogAll = f"../All Logs/{Foldername}/"


    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")

    next(logAllReader)
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        horizontalPeriodStretched = horizontalPeriod*b_two*a_two
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        
        yPath = name+"debuggerY.csv"
        xPath = name+"debuggerX.csv"
        print("a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1")
        AngleWriter,file = csvStuff.createWriter(name+"AngleDiff4Round.csv")

        yReader = csvStuff.createReader(yPath)
        xReader = csvStuff.createReader(xPath)
        for y in yReader:
            x = next(xReader)
            line = []
            for i in range(1,len(x)-1):
                gradOne = (int(y[i])-int(y[i-1]))/(int(x[i])-int(x[i-1]))
                gradTwo = (int(y[i+1])-int(y[i]))/(int(x[i+1])-int(x[i]))
                if((int(x[i])-int(x[i-1]))/a_two/b_two - int((int(x[i])-int(x[i-1]))/a_two/b_two)!=0):
                    print("Hello")
                xDif = int((int(x[i])-int(x[i-1]))/a_two/b_two)
                for j in range(0,xDif-1):
                    line.append('x')
                line.append(round(gradTwo-gradOne,5))
            AngleWriter.writerow(line)
        file.close()

 
def plot2d(xdata,ydata):
    fig,ax=plt.subplots()
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=1)
    locy.MAXTICKS= 694208142317
    locx = plticker.MultipleLocator(base=0.5)
    locx.MAXTICKS= 694208142317
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("vertical Period")
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    plt.scatter(xdata,ydata)
    plt.show()



def plot3d(xdata,ydata,zdata):
    fig = plt.figure()
    ax = Axes3D(fig)
    #ax = fig.add_subplot(111, projection='3d')
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    #locy = plticker.MultipleLocator(base=10)
    #locy.MAXTICKS= 694208142317
    #locx = plticker.MultipleLocator(base=0.1)
    #locx.MAXTICKS= 694208142317
    #ax.xaxis.set_major_locator(locx)
    #ax.yaxis.set_major_locator(locy)
    #ax.zaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("b")
    ax.zaxis.set_label_text("Steps")
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    ax.scatter(xdata,zdata,ydata,zdir='z')
    plt.show()
    #ax.show()                 

def investigateConcurrentZeros():
    Foldername = "Investigate Pattern"
    pathToLogs = f"../All Logs/{Foldername}/Logs/"
    pathToLogAll = f"../All Logs/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    globalWriter = csvStuff.createWriter(pathToLogAll+"ConcurrentZeros.csv")

    header = ["a_one","a_two","b_one","b_two","vertical Period","horizontalPeriod"]
    globalWriter.writerow(header)
           
    next(logAllReader)
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        cornerPath = name+"debuggerCorners.csv"
        #print("a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1")
        
        corners = open(cornerPath).readlines()
        corners = [x.split(",") for x in corners]

        for i in range(0,len(corners)-1):
            finished = False
            for j in range(len(corners[i])-1,len(corners[i])-steps_two+1,-1):
                if(corners[i][j]=='1' and corners[i+1][j]=='1'):
                    data = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod]
                    print(corners[i])
                    globalWriter.writerow(header)
                    globalWriter.writerow(data)
                    globalWriter.writerow(corners[i])
                    globalWriter.writerow(corners[i+1])
                    finished = True
                    break
            if(finished==True):
                continue
                #if(j==len(corners[i])-steps_two+2):
                    #data = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod]
                    #print(data)
                    #globalWriter.writerow(data)



def disPlayTime(pathtoTimeLog):
    timeReader = csvStuff.createReader(pathtoTimeLog)

    next(timeReader)
    nums=[]
    times = []
    for row in timeReader:
        a_one = int(row[0])
        a_two = int(row[1])
        numx = int(row[2])
        time = float(row[3])
        nums.append(numx)
        times.append(time)
    print(times)
    plt.scatter(nums,times)
    plt.show()
        

def disPlayVerticalPeriod(pathtoAllLog,dimension):
    timeReader = csvStuff.createReader(pathtoAllLog)

    next(timeReader)
    a=[]
    b = []
    vertical_Period = []
    for row in timeReader:
        if(len(row) >7):
            a_one = int(row[0])
            a_two = int(row[1])
            b_one = int(row[2])
            b_two = int(row[3])
            steps_two = int(row[7])
            if(dimension == 3 or b_one == 0):
                if(steps_two<20):
                    a.append(a_one/float(a_two))
                    b.append(b_one/float(b_two))
                    vertical_Period.append(steps_two)
    if(dimension==2):     
        plot2d(a,vertical_Period)
    if(dimension == 3):
        plot2d(a,vertical_Period)
        
disPlayVerticalPeriod("../Investigate Specific/Dataset/LogAll.csv",2)



def investigateConcurrentOnes():
    Foldername = "Investigate Pattern"
    pathToLogs = f"../All Logs/{Foldername}/Logs/"
    pathToLogAll = f"../All Logs/{Foldername}/"

    globalWriterOnes = csvStuff.createWriter(pathToLogAll+"concOnes.csv")
    globalWriterZeros = csvStuff.createWriter(pathToLogAll+"concZeros.csv")

    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")

    next(logAllReader)
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        horizontalPeriodStretched = horizontalPeriod*b_two*a_two
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        cornerPath = name+"debuggerCorners.csv"

        print("a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1")

        
        corners = open(cornerPath).readlines()
        corners = [x.split(",") for x in corners]
        
        

        header = ["a_one","a_two","b_one","b_two","vertical Period","horizontalPeriod","indices"]
        globalWriterOnes.writerow(header)
        globalWriterZeros.writerow(header)

        investigateRowOnes = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod]
        investigateRowZeros = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod]

        globalWriterOnes.writerow(investigateRowOnes)
        globalWriterZeros.writerow(investigateRowZeros)

        for i in range(len(corners)-steps_two-1,len(corners)-1):
            for j in range(0, horizontalPeriod):
                if(corners[i][j]=='0' and corners[i+1][j]=='0'):
                    if(len(investigateRowZeros)<=100):
                        investigateRowZeros.append(j+1)
                if(corners[i][j]=='1' and corners[i+1][j]=='1'):
                    if(len(investigateRowOnes)<=100):
                        investigateRowOnes.append(j+1)
            if(len(investigateRowOnes)>6):
                globalWriterOnes.writerow(investigateRowOnes)
                investigateRowOnes = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod]
            if(len(investigateRowZeros)>6):
                globalWriterZeros.writerow(investigateRowZeros)
                investigateRowZeros = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod]



def writeZusammenfassung():
    Foldername = "Investigate Pattern"
    pathToLogs = f"../All Logs/{Foldername}/Logs/"
    pathToLogAll = f"../All Logs/{Foldername}/"

    globalWriter = csvStuff.createWriter(pathToLogAll+"testing.csv")
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")

    next(logAllReader)
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        g_one = int(row[4])
        g_two = int(row[5])
        steps_one = int(row[6])
        steps_two = int(row[7])
        if(a_one==1 and a_two==4 and b_one==3 and b_two==4):
            horizontalPeriod = int(row[8])
            periodCase = getPeriodCase(a_two,b_two)
            horizontalPeriodStretched = horizontalPeriod*b_two*a_two
            name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
            disPath = name + "debuggerDis.csv"
            cornerPath = name+"debuggerCorners.csv"
            xPath = name + "debuggerX.csv"

            print("a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1")

            dists = open(disPath).readlines()
            dists = [x.split(",") for x in dists]

            lastDist = dists[-1]
            
            corners = open(cornerPath).readlines()
            corners = [x.split(",") for x in corners]
            lastCorners = corners[-1]

            maxZerosStart = findMaxZeros(corners[0])
            maxZerosEnd = findMaxZeros(lastCorners)

            xVals = open(xPath).readlines()
            xVals = [x.split(",") for x in xVals]
            lastX = xVals[-1]

            count = 1
            tmp = 0
            for i,x in enumerate(lastDist):
                tmp += int(x)
                if(tmp == horizontalPeriodStretched):
                    cornerPeriod = lastCorners[0:int(int(lastX[i+1])/(a_two*b_two))]
                    maxZerosInPeriod = findMaxZeros(cornerPeriod)
                    elementsInPeriod = i+1
                    break
            header = ["a_one","a_two","b_one","b_two","period case","max Zeros Start","max Zeros end","vertical Period","horizontalPeriod","verticalTranslation","index of Period","max Zeros in period"]
            globalWriter.writerow(header)
            periodTranslation = [a_one,a_two,b_one,b_two,periodCase,maxZerosStart,maxZerosEnd,steps_two,horizontalPeriod]
            count = 1
            for i in range(len(corners)-2,-1,-1):
                periodstr = "".join(cornerPeriod)
                curcornerstr = "".join(corners[i])

                if periodstr in curcornerstr:
                    periodTranslation.append(count)
                    index = curcornerstr.index(periodstr)
                    periodTranslation.append(index)
                    periodTranslation.append(maxZerosInPeriod)
                    globalWriter.writerow(periodTranslation)
                    periodTranslation = [a_one,a_two,b_one,b_two,periodCase,maxZerosStart,maxZerosEnd,steps_two,horizontalPeriod]
                    if(index == 0):
                        break
                    else:
                        count=1
                else:
                    count+=1


