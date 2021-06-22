def ggT(a,b):
    if (b == 0):
        return a
    else:
        return ggT(b, (a % b))


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