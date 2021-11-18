
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

 
def plot2d(xdata,ydata):
    fig,ax=plt.subplots()
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=1)
    locx = plticker.MultipleLocator(base=0.05)
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("Vertikale Periode")
 

    ax.grid(b= True, which='major', axis='both', linestyle='-')
    ax.scatter(xdata,ydata,s=4)
    n=5
    for index, label in enumerate(ax.yaxis.get_ticklabels()):
        print(index)
        if index % n != 0:
            label.set_visible(False)
    plt.show()



def plot3d(xdata,ydata,zdata):
    fig = plt.figure()
    ax = Axes3D(fig)
    #ax = fig.add_subplot(111, projection='3d')
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=5)
    #locy.MAXTICKS= 694208142317
    locx = plticker.MultipleLocator(base=1)
    #locx.MAXTICKS= 694208142317
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locx)
    ax.zaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("b")
    ax.zaxis.set_label_text("Steps")
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    ax.scatter(xdata,ydata,zdata,zdir='z',s=2)
    plt.show()
    #ax.show()                 


def checkErrorInTubeThickness():
    Foldername = "Dataset with Tube"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    a = []
    tubeThicknesses = []
    next(logAllReader)
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        investigatedX = 3*int(row[8])
        time = float(row[8])
        verticalTranslation = float(row[9])
        averageTubeThickness = float(row[10])
        minTubeThickness = float(row[11])
        maxTubeThickness = float(row[12])
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1"
        #print(name)
        if(investigatedX<50):
            investigatedX=50
        verticalDisPath = name+"Distances.csv"
        verticalDisReader = csvStuff.createReader(verticalDisPath)
        for row in verticalDisReader:
            if(row[0]=="x_min"):
                continue
            if(float(row[0]) <0):
                print(name,1,row[0])
            if(float(row[0])>investigatedX):
                print(name,2,row[0],investigatedX)
            if(float(row[3])<0):
                print(name,3,row[3])
            if(float(row[3])>investigatedX):
                print(name,3,row[3])


def displayVerticalTranslationAtBorder():
    Foldername = "Border specific"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    globalWriter = csvStuff.createWriter(pathToLogAll+"ConcurrentZeros.csv")
    a = []
    b= []
    bVertical = []
    avgtubeThicknesses_in_period = []
    maxtubeThicknesses = []
    total_translations = []
    verticalTranslations_in_period = []
    maxtubeThicknesses_in_period = []

    bordersa_two = [2,8,22,44]

    b = [[],[],[],[]]
    verticalTranslation_atborder = [[],[],[],[]]


    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        time = float(row[9])
        verticalTranslation = float(row[10])
        averageTubeThickness = float(row[11])
        minTubeThickness = float(row[12])
        maxTubeThickness = float(row[13])
        averageTubeThickness_in_period = float(row[14])
        verticalTranslation_in_period = float(row[15])
        #maxTubeThickness_in_period = float(row[16])
        total_translation = verticalTranslation_in_period*steps_two
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        distancesPath = name+"debuggerCorners.csv"
        a.append(a_one/float(a_two))
        avgtubeThicknesses_in_period.append(averageTubeThickness_in_period)
        verticalTranslations_in_period.append(verticalTranslation_in_period)
        if(a_two in bordersa_two and a_one==1):
            index = bordersa_two.index(a_two)
            b[index].append(b_one/b_two)
            verticalTranslation_atborder[index].append(verticalTranslation_in_period)


    
    f,([fig2,fig8],[fig22,fig44]) = plt.subplots(2,2)

    #for x in bordersx:
    #    figOne.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)
    #    figTwo.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)

    fig2.set_title('a=1/2')
    #fig2.yaxis.set_label_text("Durchschnittliche vertikale Verschiebung")
    fig2.scatter(b[0],verticalTranslation_atborder[0],s=1)

    fig8.set_title('a=1/8')
    #fig8.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig8.scatter(b[1],verticalTranslation_atborder[1],s=1)    
    
    fig22.set_title('a=1/22')
    fig22.xaxis.set_label_text("b")
    fig22.yaxis.set_label_text("Durchschnittliche vertikale Verschiebung")
    fig22.scatter(b[2],verticalTranslation_atborder[2],s=1)   

    fig44.set_title('a=1/44')
    fig44.xaxis.set_label_text("b")
    #fig44.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig44.scatter(b[3],verticalTranslation_atborder[3],s=1) 
    plt.show()

#displayVerticalTranslationAtBorder()

def displayVerticalTranslation():
    Foldername = "All Data b=0"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    globalWriter = csvStuff.createWriter(pathToLogAll+"ConcurrentZeros.csv")
    a = []
    b= []
    bVertical = []
    avgtubeThicknesses_in_period = []
    maxtubeThicknesses = []
    total_translations = []
    verticalTranslations_in_period = []
    maxtubeThicknesses_in_period = []
    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        time = float(row[9])
        verticalTranslation = float(row[10])
        averageTubeThickness = float(row[11])
        minTubeThickness = float(row[12])
        maxTubeThickness = float(row[13])
        averageTubeThickness_in_period = float(row[14])
        verticalTranslation_in_period = float(row[15])
        maxTubeThickness_in_period = float(row[16])
        total_translation = verticalTranslation_in_period*steps_two
        bordersa_two = [2,8,22,44,86]

        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        distancesPath = name+"debuggerCorners.csv"
        a.append(a_one/float(a_two))
        avgtubeThicknesses_in_period.append(averageTubeThickness_in_period)
        verticalTranslations_in_period.append(verticalTranslation_in_period)
        maxtubeThicknesses_in_period.append(maxTubeThickness_in_period)
    f,(figOne) = plt.subplots(1,1)

    #for x in bordersx:
    #    figOne.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)
    #    figTwo.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)

    locy = plticker.MultipleLocator(base=0.05)
    #locx.MAXTICKS= 694208142317
    figOne.yaxis.set_major_locator(locy)
    figOne.yaxis.grid(True)
    figOne.xaxis.set_major_locator(locy)
    figOne.xaxis.grid(True)   
    figOne.xaxis.set_label_text("a")
    figOne.yaxis.set_label_text("Durchschnittliche vertikale Verschiebung")
    figOne.scatter(a,verticalTranslations_in_period,s=1)
    
    plt.show()

#displayVerticalTranslation()

def displayTubethickness():
    Foldername = "All Data b=0"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    globalWriter = csvStuff.createWriter(pathToLogAll+"ConcurrentZeros.csv")
    a = []
    b= []
    bVertical = []
    avgtubeThicknesses_in_period = []
    maxtubeThicknesses = []
    total_translations = []
    verticalTranslations_in_period = []
    maxtubeThicknesses_in_period = []
    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        time = float(row[9])
        verticalTranslation = float(row[10])
        averageTubeThickness = float(row[11])
        minTubeThickness = float(row[12])
        maxTubeThickness = float(row[13])
        averageTubeThickness_in_period = float(row[14])
        verticalTranslation_in_period = float(row[15])
        maxTubeThickness_in_period = float(row[16])
        total_translation = verticalTranslation_in_period*steps_two
        bordersa_two = [2,8,22,44,86]

        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        distancesPath = name+"debuggerCorners.csv"
        a.append(a_one/float(a_two))
        avgtubeThicknesses_in_period.append(averageTubeThickness_in_period)
        verticalTranslations_in_period.append(verticalTranslation_in_period)
        maxtubeThicknesses_in_period.append(maxTubeThickness_in_period)
    bordersx = [1/2.,1/8.,1/22.,1/44.,1/86.]
    f,(figOne) = plt.subplots(1,1)

    #for x in bordersx:
    #    figOne.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)
    #    figTwo.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)


    figOne.set_yscale('log')
    figOne.xaxis.set_label_text("a")
    figOne.yaxis.set_label_text("Maximale Schlauchdicke")
    figOne.scatter(a,maxtubeThicknesses_in_period,s=1)
    
    #figTwo.set_yscale('log')
    #figTwo.xaxis.set_label_text("a")
    #figTwo.yaxis.set_label_text("Maximale Schlauchdicke")

    #figTwo.scatter(a,maxtubeThicknesses_in_period,s=1)

    plt.show()

#displayTubethickness()


def displayTubethicknessAtBorder():
    Foldername = "Border specific"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")
    globalWriter = csvStuff.createWriter(pathToLogAll+"ConcurrentZeros.csv")
    a = []
    b= []
    bVertical = []
    avgtubeThicknesses_in_period = []
    maxtubeThicknesses = []
    total_translations = []
    verticalTranslations_in_period = []
    maxtubeThicknesses_in_period = []

    bordersa_two = [2,8,22,44]

    b = [[],[],[],[]]
    tubeThickness_atborder = [[],[],[],[]]


    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        time = float(row[9])
        verticalTranslation = float(row[10])
        averageTubeThickness = float(row[11])
        minTubeThickness = float(row[12])
        maxTubeThickness = float(row[13])
        averageTubeThickness_in_period = float(row[14])
        verticalTranslation_in_period = float(row[15])
        #maxTubeThickness_in_period = float(row[16])
        total_translation = verticalTranslation_in_period*steps_two
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        distancesPath = name+"debuggerCorners.csv"
        a.append(a_one/float(a_two))
        avgtubeThicknesses_in_period.append(averageTubeThickness_in_period)
        verticalTranslations_in_period.append(verticalTranslation_in_period)
        if(a_two in bordersa_two and a_one==1):
            index = bordersa_two.index(a_two)
            b[index].append(b_one/b_two)
            tubeThickness_atborder[index].append(averageTubeThickness_in_period)


    
    f,([fig2,fig8],[fig22,fig44]) = plt.subplots(2,2)

    #for x in bordersx:
    #    figOne.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)
    #    figTwo.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)

    fig2.set_yscale('log')
    fig2.set_title('a=1/2')
    #fig2.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig2.scatter(b[0],tubeThickness_atborder[0],s=1)

    fig8.set_yscale('log')
    fig8.set_title('a=1/8')
    #fig8.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig8.scatter(b[1],tubeThickness_atborder[1],s=1)    
    
    fig22.set_yscale('log')
    fig22.set_title('a=1/22')
    fig22.xaxis.set_label_text("b")
    fig22.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig22.scatter(b[2],tubeThickness_atborder[2],s=1)   

    fig44.set_yscale('log')
    fig44.set_title('a=1/44')
    fig44.xaxis.set_label_text("b")
    #fig44.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig44.scatter(b[3],tubeThickness_atborder[3],s=1) 


    plt.show()

#displayTubethicknessAtBorder()



def calc_avg_verticalTranslation():
    Foldername = "All Data newio"
    pathToLogs = f"../Investigate Specific/{Foldername}/Logs/"
    pathToLogAll = f"../Investigate Specific/{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"LogAll.csv")

    tubeThicknesses = []
    next(logAllReader)
    till2 = []
    till8 = []
    till22 = []
    till44 = []
    till86 = []
    till0 = []
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        steps_two = int(row[7])
        horizontalPeriod = int(row[8])
        time = float(row[9])
        verticalTranslation = float(row[10])
        averageTubeThickness = float(row[11])
        minTubeThickness = float(row[12])
        maxTubeThickness = float(row[13])
        averageTubeThickness_in_period = float(row[14])
        verticalTranslation_in_period = float(row[15])
        bordersa_two = [2,8,22,44,86]
        a= a_one/float(a_two)
        name = pathToLogs+"a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g=1|1/"
        distancesPath = name+"debuggerCorners.csv"

        if(a>1/2.):
            till2.append(verticalTranslation_in_period)
        if(a<1/2. and a>1/8.):
            till8.append(verticalTranslation_in_period)
        if(a>1/22. and a <1/8.):
            till22.append(verticalTranslation_in_period)
        if(a>1/44. and a<1/22.):
            till44.append(verticalTranslation_in_period)
        if(a>1/86. and a<1/44.):
            till86.append(verticalTranslation_in_period)
        if(a<1/86.):
            till0.append(verticalTranslation_in_period)
        
    averages = [sum(till2)/len(till2),sum(till8)/len(till8),sum(till22)/len(till22),sum(till44)/len(till44),sum(till86)/len(till86),sum(till0)/len(till0)]
    print(averages)

#calc_avg_verticalTranslation()


def disPlayTime(pathtoTimeLog):
    timeReader = csvStuff.createReader(pathtoTimeLog)

    next(timeReader)

    nums=[]
    avg_times = []
    total_times = []
    a=[]
    b = []
    ab = []
    vertical_Periods = []
    total_steps = []

    for row in timeReader:
        if(len(row) >7):
            a_one = int(row[0])
            a_two = int(row[1])
            b_one = int(row[2])
            b_two = int(row[3])
            steps_one = int(row[6])
            steps_two = int(row[7])
            horizontal_periode = int(row[8])
            avg_time = float(row[9])
            total_step = steps_one+steps_two
            total_time = avg_time*total_step
            #if(a_one==1 and b_one==0):
            total_steps.append(total_step)
            num = 3*horizontal_periode
            if(num < 50):
                num = 50
            nums.append(num)
            a.append(a_one/float(a_two))
            ab.append((a_one/float(a_two)) +(b_one/float(b_two)) )
            avg_times.append(avg_time)
            total_times.append(total_time)
            vertical_Periods.append(steps_two)
    plt.scatter(nums,avg_times,s=2)
    plt.show()
        
#disPlayTime("../Investigate Specific/Dataset with Tube/LogAll.csv")

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
                if(steps_two<50):
                    a.append(a_one/float(a_two))
                    b.append(b_one/float(b_two))
                    vertical_Period.append(steps_two)
    if(dimension==2):     
        plot2d(a,vertical_Period)
    if(dimension == 3):
        plot2d(a,vertical_Period)
        
disPlayVerticalPeriod("../Investigate Specific/All Data/LogAll.csv",3)






























'''

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

'''