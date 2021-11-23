
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import csvStuff
import sys

##########################################################################
##                                                                      ##
##      All the functions work the same. They read the Summarylog       ##
##      which was created with "investigate_specific_parabolas.py"      ##
##      and plot the data.                                              ##
##                                                                      ##
##########################################################################


# an exception are the the functions "displayVerticalTranslationAtBorder", "verticalPeriodAtBorder" and "displayTubethicknessAtBorder"
# for these you need to create a Log for the periodcases a=1/2,1/8,1/22,1/44 with different values for b
# then you can display the Summarylog using one of the given functions


#plots a 2d graph of xdata and ydata with a grid
def plot2d(xdata,ydata):
    fig,ax=plt.subplots()
    locy = plticker.MultipleLocator(base=1)
    locx = plticker.MultipleLocator(base=0.05)
    ax.xaxis.set_major_locator(locx)
    ax.yaxis.set_major_locator(locy)
    ax.xaxis.set_label_text("a")
    ax.yaxis.set_label_text("Zeitliche Periode")
    ax.grid(b= True, which='major', axis='both', linestyle='-')
    ax.scatter(xdata,ydata,s=5)
    plt.show()


#displays the average vertical translation of the SummaryLog
def displayVerticalTranslation(path_to_Summary_Log):
    logAllReader = csvStuff.createReader(path_to_Summary_Log)
    a = []
    verticalTranslations_in_period = []
    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        verticalTranslation_in_period = float(row[11])
        a.append(a_one/float(a_two))
        verticalTranslations_in_period.append(verticalTranslation_in_period)
    f,(figOne) = plt.subplots(1,1)
    locy = plticker.MultipleLocator(base=0.05)
    figOne.yaxis.set_major_locator(locy)
    figOne.yaxis.grid(True)
    figOne.xaxis.set_major_locator(locy)
    figOne.xaxis.grid(True)   
    figOne.xaxis.set_label_text("a")
    figOne.yaxis.set_label_text("Durchschnittliche vertikale Verschiebung")
    figOne.scatter(a,verticalTranslations_in_period,s=10)
    plt.show()

#displays the Maximum tube thicknes of the SummaryLog
def displayMaximumTubethickness(path_to_Summary_Log):
    logAllReader = csvStuff.createReader(path_to_Summary_Log)
    a = []
    maxtubeThicknesses_in_period = []
    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        maxTubeThickness_in_period = float(row[12])

        a.append(a_one/float(a_two))
        maxtubeThicknesses_in_period.append(maxTubeThickness_in_period)
    f,(figOne) = plt.subplots(1,1)

    figOne.set_yscale('log')
    figOne.xaxis.set_label_text("a")
    figOne.yaxis.set_label_text("Maximale Schlauchdicke")
    figOne.scatter(a,maxtubeThicknesses_in_period,s=1)
    plt.show()

       
#displays the timeperiod of the SummaryLog
def disPlayVerticalPeriod(path_to_Summary_Log):
    timeReader = csvStuff.createReader(path_to_Summary_Log)
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
            a.append(a_one/float(a_two))
            b.append(b_one/float(b_two))
            vertical_Period.append(steps_two)
    plot2d(a,vertical_Period)

#displays the average vertical translation at the border cases
def displayVerticalTranslationAtBorder(path_to_Summary_Log):
    logAllReader = csvStuff.createReader(path_to_Summary_Log)
    a = []
    b= []
    verticalTranslations_in_period = []
    bordersa_two = [2,8,22,44]
    b = [[],[],[],[]]
    verticalTranslation_atborder = [[],[],[],[]]
    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        verticalTranslation_in_period = float(row[11])
        a.append(a_one/float(a_two))
        verticalTranslations_in_period.append(verticalTranslation_in_period)
        if(a_two in bordersa_two and a_one==1):
            index = bordersa_two.index(a_two)
            b[index].append(b_one/b_two)
            verticalTranslation_atborder[index].append(verticalTranslation_in_period)
   
    f,([fig2,fig8],[fig22,fig44]) = plt.subplots(2,2)

    fig2.set_title('a=1/2')
    fig2.yaxis.set_label_text("Durchschnittliche vertikale Verschiebung")
    fig2.scatter(b[0],verticalTranslation_atborder[0],s=1)

    fig8.set_title('a=1/8')
    fig8.scatter(b[1],verticalTranslation_atborder[1],s=1)    
    
    fig22.set_title('a=1/22')
    fig22.xaxis.set_label_text("b")
    fig22.yaxis.set_label_text("Durchschnittliche vertikale Verschiebung")
    fig22.scatter(b[2],verticalTranslation_atborder[2],s=1)   

    fig44.set_title('a=1/44')
    fig44.xaxis.set_label_text("b")
    fig44.scatter(b[3],verticalTranslation_atborder[3],s=1) 
    plt.show()

#displays the time-period at the border cases
def verticalPeriodAtBorder(path_to_Summary_Log):
    logAllReader = csvStuff.createReader(path_to_Summary_Log)
    b= []
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
        if(a_two in bordersa_two and a_one==1):
            index = bordersa_two.index(a_two)
            b[index].append(b_one/b_two)
            verticalPeriod[index].append(steps_two)
    
    f,([fig2,fig8],[fig22,fig44]) = plt.subplots(2,2)

    fig2.set_yscale('log')
    fig2.set_title('a=1/2')
    fig2.yaxis.set_label_text("Zeitliche Periode")

    fig2.scatter(b[0],verticalPeriod[0],s=1)
    fig2.set_ylim(bottom=1)

    fig8.set_yscale('log')
    fig8.set_title('a=1/8')
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
    fig44.scatter(b[3],verticalPeriod[3],s=1) 
    fig44.set_ylim(bottom=1)

    plt.show()

#displays the average tube thickness at the border cases
def displayTubethicknessAtBorder(path_to_Summary_Log):
    logAllReader = csvStuff.createReader(path_to_Summary_Log)
    a = []
    b= []
    avgtubeThicknesses_in_period = []
    bordersa_two = [2,8,22,44]
    b = [[],[],[],[]]
    tubeThickness_atborder = [[],[],[],[]]

    next(logAllReader)  #skip header
    for row in logAllReader:
        a_one = int(row[0])
        a_two = int(row[1])
        b_one = int(row[2])
        b_two = int(row[3])
        averageTubeThickness_in_period = float(row[10])
        a.append(a_one/float(a_two))
        avgtubeThicknesses_in_period.append(averageTubeThickness_in_period)
        if(a_two in bordersa_two and a_one==1):
            index = bordersa_two.index(a_two)
            b[index].append(b_one/b_two)
            tubeThickness_atborder[index].append(averageTubeThickness_in_period)
   
    f,([fig2,fig8],[fig22,fig44]) = plt.subplots(2,2)

    fig2.set_yscale('log')
    fig2.set_title('a=1/2')
    fig2.yaxis.set_label_text("Durchschnittliche Schlauchdicke")

    fig2.scatter(b[0],tubeThickness_atborder[0],s=1)

    fig8.set_yscale('log')
    fig8.set_title('a=1/8')
    fig8.scatter(b[1],tubeThickness_atborder[1],s=1)    
    
    fig22.set_yscale('log')
    fig22.set_title('a=1/22')
    fig22.xaxis.set_label_text("b")
    fig22.yaxis.set_label_text("Durchschnittliche Schlauchdicke")
    fig22.scatter(b[2],tubeThickness_atborder[2],s=1)   

    fig44.set_yscale('log')
    fig44.set_title('a=1/44')
    fig44.xaxis.set_label_text("b")
    fig44.scatter(b[3],tubeThickness_atborder[3],s=1) 
    plt.show()


def main(displaycase):
    if(displaycase == '1'): disPlayVerticalPeriod("./Logs/Dataset b!=0.csv") #displays the time-period of All Data
    if(displaycase == '2'): displayVerticalTranslation("./Logs/Dataset b!=0.csv") #displays the average vertical translation in the time period of All Data   
    if(displaycase == '3'): displayMaximumTubethickness("./Logs/Dataset b!=0.csv")  #displays the maximum tube thickness in the time-period
    if(displaycase == '4'): displayVerticalTranslationAtBorder("./Logs/Dataset bordercases.csv") #displays the average vertical translation at the border-cases
    if(displaycase == '5'): verticalPeriodAtBorder("./Logs/Dataset bordercases.csv") #displays the time-period at the border cases
    if(displaycase == '6'): displayTubethicknessAtBorder("./Logs/Dataset bordercases.csv") #displays the average tube thickness at the border cases

displaycase = sys.argv[1]
main(displaycase)