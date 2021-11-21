import csvStuff
from difflib import SequenceMatcher
import matplotlib.pyplot as plt


def getFirstIndex(current,next):
    for i in range(0,len(next)):
        for j in range(0,len(current)):
            if(int(next[i]) == int(current[j])):
                return j
            if(int(next[i])<int(current[j])):
                break
    return -1

def getLastIndex(current,next):
    for i in range(len(next)-1,0,-1):
        for j in range(len(current)-1,0,-1):
            if(int(next[i]) == int(current[j])):
                return j
            if(int(next[i])>int(current[j])):
                break
    return -1



def getDifference(current, next):
    index_front = getFirstIndex(current,next)
    index_back = getLastIndex(current,next)
    if(index_front==-1  or index_back==-1):
        raise ValueError
    return index_front,index_back

def createMaxDifferencesLog():
    Foldername = "Dataset with Tube"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    changeWriter,changeFile = csvStuff.createWriter(pathToLogAll+"change.csv")
    a = []
    maxChanges = []
    next(logAllReader)
    for row in logAllReader:

        a_one = int(row[0])
        a_two = int(row[1])
        #if(a_one != 1 or a_two != 58):
        #    continue
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        investigatedX = 3*int(row[8])
        time = float(row[8])
        verticalTranslation = float(row[9])
        averageTubeThickness = float(row[10])
        minTubeThickness = float(row[11])
        maxTubeThickness = float(row[12])
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        print(name)
        if(investigatedX<50):
            investigatedX=50
        xValPath = name+"xValues.csv"
        xReader = csvStuff.createReader(xValPath)
        changes,changes_before,changes_after = 0,0,0
        for row in xReader:
            cur = row[2:]
            nex = next(xReader)[2:]
            index_front, index_back = getDifference(cur, nex)
            cur_changes_before = index_front
            cur_changes_after = len(cur)-1-index_back
            cur_changes = cur_changes_after+cur_changes_before
            changes = max(changes,cur_changes)
            changes_before = max(changes_before,cur_changes_before)
            changes_after = max(changes_after,cur_changes_after)
        
        changeWriter.writerow([a_one/float(a_two),changes_before,changes_after,changes,investigatedX])

def displayMaxDifferences():
    Foldername = "Dataset with Tube"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    changeReader = csvStuff.createReader(pathToLogAll+"change.csv")
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

