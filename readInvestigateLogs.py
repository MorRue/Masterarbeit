
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from mpl_toolkits.mplot3d import Axes3D



import math
import calc
import csvStuff

def plot2d(xdata,ydata):
    fig,ax=plt.subplots()
    #ax.set_xticklabels([]) 
    #ax.set_yticklabels([])
    locy = plticker.MultipleLocator(base=1)
    locx = plticker.MultipleLocator(base=0.05)
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("Zeitliche Periode")
 

    ax.grid(b= True, which='major', axis='both', linestyle='-')
    ax.scatter(xdata,ydata,s=5)
    #n=5
    #for index, label in enumerate(ax.yaxis.get_ticklabels()):
    #    if index % n != 0:
    #        label.set_visible(False)
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
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
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
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
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
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
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
    figOne.scatter(a,verticalTranslations_in_period,s=10)
    
    plt.show()

displayVerticalTranslation()

def displayTubethickness():
    Foldername = "All Data b=0"
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"Summary.csv")
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


def verticalPeriodAtBorder():
    Foldername = "Border specific"
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"Summary.csv")
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
    verticalPeriod = [[],[],[],[]]


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
            verticalPeriod[index].append(steps_two)


    
    f,([fig2,fig8],[fig22,fig44]) = plt.subplots(2,2)

    #for x in bordersx:
    #    figOne.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)
    #    figTwo.plot([x,x],[-0.5,1],'-',c='orange',linewidth = 1)

    fig2.set_yscale('log')
    fig2.set_title('a=1/2')
    #fig2.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig2.scatter(b[0],verticalPeriod[0],s=1)
    fig2.set_ylim(bottom=1)

    fig8.set_yscale('log')
    fig8.set_title('a=1/8')
    #fig8.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig8.scatter(b[1],verticalPeriod[1],s=1)    
    fig8.set_ylim(bottom=1)


    fig22.set_yscale('log')
    fig22.set_title('a=1/22')
    fig22.xaxis.set_label_text("b")
    fig22.yaxis.set_label_text("Zeitliche Periode")
    fig22.scatter(b[2],verticalPeriod[2],s=1)   
    fig22.set_ylim(bottom=1)


    fig44.set_yscale('log')
    fig44.set_title('a=1/44')
    fig44.xaxis.set_label_text("b")
    #fig44.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig44.scatter(b[3],verticalPeriod[3],s=1) 
    fig44.set_ylim(bottom=1)


    plt.show()

#verticalPeriodAtBorder()

def displayTubethicknessAtBorder():
    Foldername = "Border specific"
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"Summary.csv")
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
    pathToLogs = f"../{Foldername}/Logs/"
    pathToLogAll = f"../{Foldername}/"
    logAllReader = csvStuff.createReader(pathToLogAll+"Summary.csv")

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
        
#disPlayTime("../Dataset with Tube/Summary.csv")

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
        
#disPlayVerticalPeriod("../All Data b=0/Summary.csv",3)

