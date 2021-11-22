import csvStuff
import matplotlib.pyplot as plt

# get the Index of the first element in "current" which is also in "next"
def getFirstIndex(current,next):
    for i in range(0,len(next)):
        for j in range(0,len(current)):
            if(int(next[i]) == int(current[j])):
                return j
            if(int(next[i])<int(current[j])):
                break
    return -1

# get the Index of the last element in "current" which is also in "next"
def getLastIndex(current,next):
    for i in range(len(next)-1,0,-1):
        for j in range(len(current)-1,0,-1):
            if(int(next[i]) == int(current[j])):
                return j
            if(int(next[i])>int(current[j])):
                break
    return -1

# get the number of different elements in current and next
def getDifference(current, next):
    index_front = getFirstIndex(current,next)
    index_back = getLastIndex(current,next)
    if(index_front==-1  or index_back==-1):
        raise ValueError
    return index_front,index_back

#creates a csv which displays the how much changes the correction happened
#in the Peelings, which were made in the Folder created by "investigate_specific_parabolas"
#
#ATTENTION: the "writeLogs" variable in "investigate_specific_parabolas" needed to be turned on, to make it work!
#
def createMaxDifferencesLog(pathToFolder):
    pathToLogs = f"{pathToFolder}/Logs/"
    pathToLogAll = f"{pathToFolder}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    changeWriter,changeFile = csvStuff.createWriter(pathToLogAll+"change.csv")
    next(logAllReader)
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        investigatedX = 3*int(row[8])   #3*horizontalPeriod
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        print(name)
        if(investigatedX<50):   #if 3*horizontalPeriod was smaller then 50, 50 x-values were investigated
            investigatedX=50
        xValPath = name+"xValues.csv"
        xReader = csvStuff.createReader(xValPath)
        changes,changes_before,changes_after = 0,0,0
        for row in xReader: #goes through all Peelings and writes the most changes in the file
            cur = row[2:]  #first two values are the strings: "vorher" and "xVal"
            nex = next(xReader)[2:] #first two values are the strings: "nachher" and "xVal"
            index_front, index_back = getDifference(cur, nex)
            cur_changes_before = index_front
            cur_changes_after = len(cur)-1-index_back
            cur_changes = cur_changes_after+cur_changes_before
            changes = max(changes,cur_changes)  #maximum number of changes in total
            changes_before = max(changes_before,cur_changes_before) #maximum number of changes in [0,H]
            changes_after = max(changes_after,cur_changes_after)    #maximum number of changes in [2H,3H]
        changeWriter.writerow([a_one/float(a_two),changes_before,changes_after,changes,investigatedX])


#displays the results created by "createMaxDifferencesLog" in the File
def displayMaxDifferences(pathToFile):
    changeReader = csvStuff.createReader(pathToFile)
    a = []
    maxChanges = []
    percentChanges = []
    for row in changeReader:
        a.append(float(row[0]))
        numPoints = int(row[4])
        maxChanges.append(int(row[3]))
        percentChanges.append(100*int(row[3])/numPoints)
    f,(figOne) = plt.subplots(1,1)
    figOne.xaxis.set_label_text("a")
    figOne.yaxis.set_label_text("Maximale Anzahl an korrigierten Punkten")
    figOne.scatter(a,maxChanges)
    plt.show()

#createMaxDifferencesLog()
displayMaxDifferences()

