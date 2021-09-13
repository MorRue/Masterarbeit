from matplotlib.ticker import Formatter

import calc
import csvStuff

Foldername = "Investigate 1|22 new"
pathToLogs = f"../All Logs/{Foldername}/Logs/"
pathToLogAll = f"../All Logs/{Foldername}/"

globalWriter = csvStuff.createWriter(pathToLogAll+"InvestigateTranslationShort.csv")
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
    horizontalPeriod = int(row[8])
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

    xVals = open(xPath).readlines()
    xVals = [x.split(",") for x in xVals]
    lastX = xVals[-1]

    count = 1
    tmp = 0
    for i,x in enumerate(lastDist):
        tmp += int(x)
        if(tmp == horizontalPeriodStretched):
            cornerPeriod = lastCorners[0:int(int(lastX[i+1])/(a_two*b_two))]
            elementsInPeriod = i+1
            break
    header = ["a_one","a_two","b_one","b_two","vertical Period","horizontalPeriod","elementsInPeriod","verticalTranslation","index of Period"]
    globalWriter.writerow(header)
    periodTranslation = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod,elementsInPeriod]
    count = 1
    for i in range(len(corners)-2,-1,-1):
        periodstr = "".join(cornerPeriod)
        curcornerstr = "".join(corners[i])

        if periodstr in curcornerstr:
            periodTranslation.append(count)
            index = curcornerstr.index(periodstr)
            periodTranslation.append(index)
            globalWriter.writerow(periodTranslation)
            periodTranslation = [a_one,a_two,b_one,b_two,steps_two,horizontalPeriod,elementsInPeriod]
            if(index == 0):
                break
            else:
                count=1
        else:
            count+=1
