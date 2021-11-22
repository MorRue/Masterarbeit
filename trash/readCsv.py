
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D

import calc
import csvStuff



# 1. PeriodenStartIndex bei dis_vorher finden
# 2. PeriodenEndIndex bei disvorher finden
# 3. halbe Periode zu jeder Seite rausgehen und gucken ob es stimmt
#	-> bei Ungleichheit Peeling i und x Wert ausgeben
#	
# 4. PeriodenStartIndex bei dis_nachher finden mittels x-Wert von 1. 
# 5. PeriodenEndIndex bei dis_nachher finden
#
# (6. x Werte von Endindex von vorher und nachher vergleichen -> unnötig)
# 7. y-Werte von PeriodenStartIndex undPeriodenEndIndex vergleichen
#	-> bei ungleichHeit sagen was falsch ist!


def testHullCorrection(pathToLog,a_one,a_two,b_one,b_two,g_one,g_two):
    logDisReader = csvStuff.createReader(pathToLog + "/debuggerDis.csv")
    logXReader = csvStuff.createReader(pathToLog + "/debuggerX.csv")
    logYReader = csvStuff.createReader(pathToLog + "/debuggerY.csv")

    horizontalPeriod = calc.getStretchedHorizontalPeriod(a_one,a_two,b_one,b_two,g_one,g_two)
    for row in logDisReader:
        xValues = next(logXReader)
        yValues = next(logYReader)
        length = len(row)-2
        startIndex = int(length/3)   #since the row has roughly 3*Period length and first two are not just for naming
        endIndex = calc.getEndIndex(row[2:],horizontalPeriod,startIndex)
        if(endIndex==-1):
            print(horizontalPeriod)
            print(row[startIndex:])
            raise Exception("Period not found!")
        tmp = calc.testXdata(row[2:],startIndex,endIndex)
        if(tmp ==0): 
            print("all fine till now!")
        else: 
            raise Exception("Problem")
        
        nachherStartIndex = 0
        nachherX = next(logXReader)
        nachherY = next(logYReader)
        nachherDis = next(logDisReader)
        for i in range(2,len(nachherX)):
            if(nachherX[i]==xValues[startIndex]):
                nachherStartIndex = i
                break
        if(nachherStartIndex==0):
            raise Exception("Startindex in corrected Hull not found!")
        else:
            nachherEndIndex = calc.getEndIndex(nachherDis[2:],horizontalPeriod,nachherStartIndex)
        if(nachherEndIndex ==-1):
            raise Exception("Endindex in corrected Hull not found!")
        
        if(nachherY[nachherStartIndex] != yValues[startIndex]):
            print("y-Werte an Startindex unterschiedlich")
            return

        if(nachherY[nachherEndIndex] != yValues[endIndex]):
            print("y-Werte an Endindex unterschiedlich")
            return
        print("-----all good----  nachherStartIndex =",nachherStartIndex,"   startindex = ",startIndex, " nachherEndIndex = ", nachherEndIndex, "  endIndex = ",endIndex)



def findHorziontalPeriod(reader,a_one,a_two,b_one,b_two,g_one,g_two):
    next(reader) #skip headline
    for row in reader:
            a_one_tmp = int(row[0])
            a_two_tmp = int(row[1])
            b_one_tmp = int(row[2])
            b_two_tmp = int(row[3])
            g_one_tmp = int(row[4])
            g_two_tmp = int(row[5])
            #steps_one_tmp = int(row[6])
            #steps_two_tmp = int(row[7])
            horizontalPeriod_tmp = int(row[8])
            if(a_one_tmp == a_one and a_two_tmp == a_two and b_one_tmp == b_one and b_two_tmp == b_two and g_one_tmp==g_one and g_two_tmp == g_two):
                return horizontalPeriod_tmp
    return -1


def findVerticalPeriod(reader,a_one,a_two,b_one,b_two,g_one,g_two):
    next(reader) #skip headline
    for row in reader:
            a_one_tmp = int(row[0])
            a_two_tmp = int(row[1])
            b_one_tmp = int(row[2])
            b_two_tmp = int(row[3])
            g_one_tmp = int(row[4])
            g_two_tmp = int(row[5])
            steps_one_tmp = int(row[6])
            verticalPeriod_tmp = int(row[7])
            if(a_one_tmp == a_one and a_two_tmp == a_two and b_one_tmp == b_one and b_two_tmp == b_two and g_one_tmp==g_one and g_two_tmp == g_two):
                return steps_one_tmp,verticalPeriod_tmp
    return -1,-1

def findVelocity(pathToLogs,a_one,a_two,b_one,b_two,g_one,g_two, firstOccurence,verticalPeriod):
    #logAllReader = csvStuff.createReader(pathToLogAll + "/LogAll.csv")
    logXReader = csvStuff.createReader(pathToLogs + "/debuggerX.csv")
    logYReader = csvStuff.createReader(pathToLogs + "/debuggerY.csv")
    #logDisReader =csvStuff.createReader(pathToLogs + "/debuggerDis.csv")
    #firstOccurence, verticalPeriod = findVerticalPeriod(logAllReader,a_one,a_two,b_one,b_two,g_one,g_two)
    if(verticalPeriod == -1):
        raise Exception("Case ,a_one,a_two,b_one,b_two,g_one,g_two =",a_one,a_two,b_one,b_two,g_one,g_two, "not found")
    
    #get to the First Occurence of the Period with xval[0] == 0
    for i in range(0,firstOccurence):
        next(logYReader)
        next(logYReader)
        next(logXReader)
        next(logXReader)
    next(logXReader)
    xStart = next(logXReader)
    next(logYReader)
    yStart = next(logYReader)

    #get to the Last Occurence of the Period with xval[0] == 0
    for i in range(0,verticalPeriod-1):
        next(logYReader)
        next(logYReader)
        next(logXReader)
        next(logXReader)
    next(logXReader)
    xEnd = next(logXReader)
    next(logYReader)
    yEnd = next(logYReader)

    #check if the xValues are actually the same
    if(xStart == xEnd):
        print((int(yEnd[2])-int(yStart[2]))/(a_two*b_two))
        return (int(yEnd[2])-int(yStart[2]))/(a_two*b_two)
    else:
        raise Exception("Case ,a_one,a_two,b_one,b_two,g_one,g_two =",a_one,a_two,b_one,b_two,g_one,g_two,"  x-Values different")


# Stimmt die Ursprungshülle/werte? 
#
#Arraywerte = x',y'
#	-> wie überprüfen?
#		1. f(x) ausrechnen
#		2. dif = Hüllenwert-f(x) berechnen
#		3. wenn dif >= 1 : Ausgabe von x und f(x) und Hüllenwert
#	Sowohl mit gestretched, als auch mit normal!
#	Stretchung = a_two * b_two
#	
#	x   = x'/(a_two*b_two)
#	y_1 = f(x)
#	y_2 = y'/(a_two*b_two)
#	
#	dif_1 = y_1-y_2
#	
#	y_3 = f(x')
#	dif_2 = y' - y_3

def testFirstHull(pathToLogAll, pathToLogs,a_one,a_two,b_one,b_two,g_one,g_two):
    logAllReader = csvStuff.createReader(pathToLogAll + "/LogAll.csv")
    
    logXReader = csvStuff.createReader(pathToLogs + "/debuggerX.csv")
    logYReader = csvStuff.createReader(pathToLogs + "/debuggerY.csv")
    logDisReader =csvStuff.createReader(pathToLogs + "/debuggerDis.csv")

    horizontalPeriod = findHorziontalPeriod(logAllReader,a_one,a_two,b_one,b_two,g_one,g_two)
    if(horizontalPeriod == -1):
        raise Exception("Case not found!")
        
    if(calc.getHorizontalPeriod(a_two,b_two) != horizontalPeriod):
        raise Exception("Period different!")
    
    xValues = next(logXReader)
    yValues = next(logYReader)
    xdisValues = next(logDisReader)
    maxX = 0
    maxY = 0
    maxdif = 0
    for i in range(2,len(xValues)):
        x = int(xValues[i])/(a_two*b_two)
        y_one = (x*x*a_one/a_two) + (x*b_one/b_two)
        y_two = int(yValues[i])/(a_two*b_two)
        dif_one = y_two - y_one     #unstretched: difference between hull y-value and calculated y-value 
        print(dif_one, x ,)
        y_three = (int(xValues[i])*int(xValues[i])*a_one/a_two) + (int(xValues[i])*b_one/b_two)
        dif_two = int(yValues[i]) - y_three #stretched: difference between hull y-value and calculated y-value
        if(dif_one >=maxdif):
            maxX = x
            maxY = y_one
            maxdif = dif_one
    return maxdif, maxX, maxY
        



def plot(xdata,ydata):
    intervals = float(gridToInvestigate/float(10)) #Spacing between each line of the displayed grid -> NOT WORKING WTF
    fig,ax=plt.subplots()
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=5)
    locy.MAXTICKS= 694208142317
    locx = plticker.MultipleLocator(base=0.01)
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
    locy = plticker.MultipleLocator(base=10)
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

def createVelocityLog(pathToLogAll, pathToLogs):
    logAllReader = csvStuff.createReader(pathToLogAll + "/LogAll.csv")
    logVelocityWriter = csvStuff.createWriter(pathToLogAll+"/LogVelocity.csv")
    header = next(logAllReader)
    header.append("Velocity")
    logVelocityWriter.writerow(header)

    for row in logAllReader:
        if(len(row) >= 7):
            a_one = row[0]
            a_two = row[1]
            b_one = row[2]
            b_two = row[3]
            g_one = row[4]
            g_two = row[5]
            firstOccurence = int(row[6])
            verticalPeriod = int(row[7])    
            horizontalPeriod = int(row[8])
            pathToLogs_tmp = pathToLogs +"/a="+a_one+"|"+a_two+" b="+ b_one +"|"+b_two+" g=1|1/"
            velocity = findVelocity(pathToLogs_tmp,int(a_one),int(a_two),int(b_one),int(b_two),int(g_one),int(g_two), firstOccurence,verticalPeriod)
            row.append(velocity)
            logVelocityWriter.writerow(row)

def main():
    for row in logReader:
        if(len(row) >= 7):
            a_one = int(row[0])
            a_two = int(row[1])
            b_one = int(row[2])
            b_two = int(row[3])
            g_one = int(row[4])
            g_two = int(row[5])
            steps_one = int(row[6])
            steps_two = int(row[7])


            '''
            #
            #uncomment to plot verticalPeriod results
            #

            if(g_two == gridToInvestigate):
                aone.append(a_one)
                atwo.append(a_two)
                xdata.append(a_one/float(a_two))
                zdata.append(b_one/float(b_two))
                ydataFirst.append(steps_one)
                ydataSecond.append(steps_two)
            '''


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

def printBorders(a,steps):
    aMin = []
    aOneMin = []
    aTwoMin = []
    aMax = []
    aOneMax = []
    aTwoMax = []
    stepsOrdered =[]
    for i in range(0,len(steps)):
        if(not (steps[i] in stepsOrdered)):
            aMin.append(99999999)
            aMax.append(0)
            aOneMin.append(0)
            aTwoMin.append(0)
            aOneMax.append(0)
            aTwoMax.append(0)            

            stepsOrdered.append(steps[i])
    
    stepsOrdered.sort()
    for i in range(0,len(a)):
        index = stepsOrdered.index(steps[i])
        #print("steps",steps[i])
        #print("ordered",stepsOrdered[index])
        if(a[i]>aMax[index]):
            aMax[index]=a[i]
            aOneMax[index]=aone[i]
            aTwoMax[index]=atwo[i]
        if(a[i]<aMin[index]):
            aMin[index]=a[i]
            aOneMin[index]=aone[i]
            aTwoMin[index]=atwo[i]
    print(len(stepsOrdered))
    for i in range(0,len(aMin)):
        print(stepsOrdered[i],"..von..",round(aMin[i],7),"=",aOneMin[i],"|",aTwoMin[i],"..bis..",round(aMax[i],7),"=",aOneMax[i],"|",aTwoMax[i])



pathToLogs = "../All Logs/Loga=1|1|/Logs/"
pathToLogAll = "../All Logs/Loga=1|128"

createVelocityLog(pathToLogAll,pathToLogs)
#findVelocity(pathToLogAll,pathToLogs,1,128,1,7,1,1)
#testHullCorrection(pathToLogs,1,128,1,7,1,1)


#GLOBAL CSV-READER-STUFF

#logfilename = path + "LogAll.csv" 
#logReader = csvStuff.createReader(logfilename)
#next(logReader)



#GLOBAL PLOTSTUFF
xdata = []  #a1/a2
aone = []
atwo = []
zdata = []  #b1/b2
ydataFirst = []
ydataSecond = []
gridToInvestigate = 1

#main()
#printBorders(xdata,ydataSecond)
#plot(xdata,ydataSecond)
#plot3d(xdata,ydataSecond,zdata)


'''
testReader_one = csvStuff.createReader("../All Logs/BorderCheck2708Logs/a=4999|110000 b=2|3 g=1|1/debuggerY.csv")
testReader_two = csvStuff.createReader("../All Logs/BorderCheck2708Logs/a=4999|110000 b=1|3 g=1|1/debuggerY.csv")

print(next(testReader_one)[4])
print(next(testReader_two)[4])


#print(testFirstHull("../All Logs/Loga=1|214", "../All Logs/Loga=1|214/Logs/a=1|214 b=1|1 g=1|1",1,214,1,1,1,1))
'''
