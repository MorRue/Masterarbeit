##################################################################################
##                                                                              ##
##   functions to calculate the distance from the approximations to ax^2 +bx    ##
##                                                                              ##
##################################################################################



#returns the x-value and distance of the point with the furthest distance
def getMaxDistance(a_one,a_two,b_one,b_two,xVals,yVals):
    max = 0
    x = 0
    for i in range(0,len(xVals)-1): #go through all linear pieces of the approximation and check the distance to ax^2+bx
        #stretch everything back
        x_from= xVals[i]/(a_two*b_two)
        x_to = xVals[i+1]/(a_two*b_two)
        f_x_from = yVals[i]/(a_two*b_two)
        f_x_to = yVals[i+1]/(a_two*b_two)
        x_tmp,distance = getDistance(a_one,a_two,b_one,b_two,x_from,x_to,f_x_from,f_x_to)
        if(distance>max):
            max = distance
            x = x_tmp
    return x,max


# returns the x-value and distance of the point with the smallest distance
# since the corners have the minimum distance, only the distance at them
# need to be investigated
def getMinDistance(a_one,a_two,b_one,b_two,xVals,yVals):
    min = -1
    x = 0
    for i in range(0,len(xVals)):
        #stretch everything back
        xVal= xVals[i]/(a_two*b_two)
        yVal = yVals[i]/(a_two*b_two)         
        f_xVal =  (a_one/float(a_two)) * (xVal**2) + (b_one/float(b_two)) * xVal
        distance =  yVal - f_xVal
        if(distance<min or min==-1):
            min = distance
            x = xVal
    return x,min

def getDistance(a_one,a_two,b_one,b_two,x_from,x_to,f_x_from,f_x_to):
    
    # Explanation:
    # distance = mx+b-f(x)
    # distance' = m-f'(x)   mit m = (f_x_to-f_x_from)/(x_to-x_from)
    # distance' = 0 <=> f'(x) = m
    m = (f_x_to-f_x_from)/(x_to-x_from)
    
    # Explanation:
    # f'(x) =2*a*x + b
    # f'(x) = m <=> x = (m-b)/2a
    x_extreme = (m-(b_one/b_two))*a_two/(2*a_one)
    f_x_extreme = (a_one/a_two) * (x_extreme**2) + (b_one/b_two) * x_extreme

    # Explanation:
    # there exists an extremum inbetween x_from and x_to
    # it is x_extreme
    if(x_from <= x_extreme and x_extreme <= x_to):
        distance = m*x_extreme + f_x_to - m*x_to - f_x_extreme
        g_x_extreme = m*x_extreme + f_x_to - m*x_to
        return x_extreme,distance

    #otherwise there is no maximum distance inbetween the corners and therefore
    #one of the cornerpoints has maximum distance from the function
    #the maximum distance is therefore the max of these two
    else:
        F_x_from = (a_one/a_two) * (x_from**2) + (b_one/b_two) * x_from
        F_x_to = (a_one/a_two) * (x_to**2) + (b_one/b_two) * x_to
        dis_x_from = m*x_from + f_x_to - m*x_to - F_x_from
        dis_x_to =m*x_to + f_x_to - m*x_to - F_x_to
        if(dis_x_from>dis_x_to):
            return x_from,dis_x_from
        else:
            return x_to,dis_x_to
 