import csv
from os import read
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

import calc
import csvStuff




logfilename = "LogNew.csv" 
logReader = csvStuff.createReader(logfilename)
next(logReader)
for row in logReader:
    row = next(logReader)
    a_one = int(row[0])
    a_two = int(row[1])
    b_one = int(row[2])
    b_two = int(row[3])
    g_one = int(row[4])
    g_two = int(row[5])
    steps_one = int(row[6])
    steps_two = int(row[7])
    grid = calc.getGrid(g_one, g_two, a_two, b_two)
    filename = "LogsNew/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)+"/debuggerY.csv"
    print(filename)
    reader = csvStuff.createReader(filename)
    j = 0
    next(reader)
    for i in range(0,2*(steps_one)):
        next(reader)
        j = j+1
    yValueStartPeriod = int(next(reader)[2])

    for i in range(0,2*steps_two-1):
        next(reader)

    yValueEndPeriod = int(next(reader)[2])
    if(yValueEndPeriod- yValueStartPeriod - grid != 0):
        print("-------------------------")
        print("PROBLEM : ",filename)
        print("-------------------------")





'''
max = 0

b_one = 0
b_two = 1
g_one = 1

k=1

while(k<1000):
    g_two = k
    for j in range(1,10):
        for i in range(j,20):
            a_one = j
            a_two = i

            if(calc.ggT(a_one,a_two)!=1):
                continue
            name = "LogsNew/a="+str(a_one)+"|"+str(a_two)+" b="+str(b_one)+"|"+str(b_two)+" g="+str(g_one)+"|"+str(g_two)+"/debuggerX.csv"
            reader = csvStuff.createReader(name)
            for row in reader:
                tmp =len(row)-len(next(reader))
                if(tmp>max):
                    max = tmp
                    print(max)
'''