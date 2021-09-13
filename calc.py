def ggT(a,b):
    if (b == 0):
        return a
    else:
        return ggT(b, (a % b))

def getInt(a):
    return int(round(a,0))

#returns endIndex of Period in x-Values
def getEndIndex(xValues, horizontalPeriod,startIndex):
    tmp = 0
    for i in range(startIndex,len(xValues)):
        tmp += int(xValues[i])
        if(tmp == horizontalPeriod):
            return i
    return -1


def stretchArray(yData,factor):
    output = []
    for x in yData:
        output.append(x*factor)
    return output

#tests if the period continues for a third of the whole thing to the left and right
def testXdata(xValues,startIndex,endIndex):
    periodValues = xValues[startIndex:endIndex+1]
    #tests right side of xValues
    tmp = 0
    for i in range(endIndex+1, endIndex + int(((endIndex - startIndex)/3))):
        if(xValues[i] != xValues[startIndex+tmp]):
            print("Problem: Werte ungleich rechte Seite bei Index", i, "von", len(xValues))
            return -1
        tmp +=1
    
    tmp = 0
    for i in range(startIndex-1, startIndex - int(((endIndex - startIndex)/3)),-1):
        if(xValues[i] != xValues[endIndex-tmp]):
            print("Problem: Werte ungleich rechte Seite bei Index", i, "von", len(xValues))
            return -1
        tmp +=1
    return 0

def getHorizontalPeriod(a,b):
    periodCase = getPeriodCase(a,b)
    return getPeriod(periodCase,a,b)


def getPeriod(periodCase,a, b):
    if(periodCase=='a'):
        period = getInt(a*b/ggT(a,b))
    elif(periodCase=='b'):
        a_half = getInt(a/2)
        period =getInt(a_half*b/ggT(a_half,b))
    elif(periodCase=='c'):
        period = getInt(a*b/ggT(a,b))
    elif(periodCase=='d'):
        period = getInt(a*b/ggT(a,b))
    elif(periodCase=='e'):
        a_half = getInt(a/2)
        period = getInt(a_half*b/ggT(a,b))
    elif(periodCase=='f'):
        a_half = getInt(a/2)
        period = a_half
    return period   

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


def getStretchedHorizontalPeriod(a_one,a_two,b_one,b_two,g_one,g_two):
    if b_one == 0:
        a_one_stretched = a_one * g_one
        a_two_stretched = a_two * g_two
        a_one_stretched, a_two_stretched = bruchKuerzen(a_one_stretched,a_two_stretched)
        if(a_two_stretched%4 == 0):
            a_two_stretched = a_two_stretched*g_two*a_two*b_two
            return a_two_stretched/2
        else:
            a_two_stretched = a_two_stretched*g_two*a_two*b_two
            return a_two_stretched
    else:
        a_one_stretched = a_one * g_one
        a_two_stretched = a_two * g_two
        a_one_stretched, a_two_stretched = bruchKuerzen(a_one_stretched,a_two_stretched)

        b_one_stretched = b_one #* g_one
        b_two_stretched = b_two #* g_two
        b_one_stretched, b_two_stretched = bruchKuerzen(b_one_stretched,b_two_stretched)
        periodCase = getPeriodCase(a_two_stretched,b_two_stretched)
        if(periodCase==0):
            print("Problem")
            return
        period = getPeriod(periodCase,a_two_stretched,b_two_stretched)
        period_stretched =period*g_two*a_two*b_two
        return period_stretched

def bruchKuerzen(a,b):
    div = ggT(a,b)
    a_out = a/div
    b_out = b/div
    return a_out,b_out


def getGrid(g_onein,g_twoin,a_twoin,b_twoin):
    return g_onein*g_twoin*a_twoin * b_twoin



def calc_distances_one(array):
    output = []
    for i in range(0,len(array)-1):
        output.append((array[i+1]-array[i]))
    return output


def getPeriodDistances(startIndex,endIndex, period, distances):
    sum = 0
    periodDistances =[]
    for i in range(startIndex,endIndex):
            sum+=distances[i]
            periodDistances.append(distances[i])
            if(sum == period):
                return periodDistances
            if(sum>period):
                return -1
'''
def findPeriod(xdata,period):
    sum = 0
    for i in range(1,len(xdata)):
        sum+=xdata[i]
        print(sum)
        if(sum == period):
            print("i=",i)
            print("Period =",sum)
            print("first",xdata[1:i+1])
            print("second", xdata[i+1:2*i+1])
            print("third", xdata[2*i+1:3*i+1])
            if(xdata[1:i+1]==xdata[i+1:2*i+1] and xdata[1:i+1]== xdata[2*i+1:3*i+1]):
                print("success, Periode =", period/(g_two*g_two*a_two*b_two))
            return
'''