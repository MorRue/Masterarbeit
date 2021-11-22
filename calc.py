#returns the gcd
def ggT(a,b):
    if (b == 0):
        return a
    else:
        return ggT(b, (a % b))

#rounds a and returns it as an integer
def getInt(a):
    return int(round(a,0))


#returns a/gcd(a,b) and b/gcd(a,b)
def bruchKuerzen(a,b):
    div = ggT(a,b)
    a_out = a/div
    b_out = b/div
    return a_out,b_out

#collects all the differences between following elements of "array" and returns them
def calc_distances_one(array):
    output = []
    for i in range(0,len(array)-1):
        output.append((int(array[i+1])-int(array[i])))
    return output

#sums up the elements of "distances" starting from startIndex till they sum up to "period"
#returns all elements of "distances", which are summed up this way
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



# receives an ordered set of points, where xdata and ydata are the x- and y-Values of the points
#
#  calculates and returns bottom convex hull
# Algorithm taken from : https://mycampus.imp.fu-berlin.de/access/content/group/e01596a9-96d7-4004-9a5b-ce451671435e/Folien/Geometrie.pdf
#
def make_para_convex(xdata,ydata):
    xdataHull = []
    ydataHull = []

    xdataHull.append(xdata[0])
    ydataHull.append(ydata[0])
    l = 0
    for k in range(1,len(xdata)):
        if(l>=1):
            gradOne = (ydataHull[l]-ydataHull[l-1]) * (xdata[k]-xdataHull[l])
            gradTwo = (ydata[k]-ydataHull[l]) * (xdataHull[l]-xdataHull[l-1])
            while(l>=1 and gradOne >= gradTwo): # check if righTurn or straith line and if so, remove the point from the set
                xdataHull.pop()
                ydataHull.pop()
                l -= 1
                if(l>=1):
                    gradOne = (ydataHull[l]-ydataHull[l-1]) * (xdata[k]-xdataHull[l])
                    gradTwo = (ydata[k]-ydataHull[l]) * (xdataHull[l]-xdataHull[l-1])
        l += 1
        xdataHull.append(xdata[k])  # append next possible value to convex hull
        ydataHull.append(ydata[k])
    return xdataHull,ydataHull



