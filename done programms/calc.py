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
