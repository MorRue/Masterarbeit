import csv
import pandas as pd


#creates a CSV and an object "writer" ro write on it
def createWriter(fileName):
    csv_file = open(fileName, "w")
    writer = csv.writer(csv_file)
    return writer,csv_file

#creates an object "reader", to read an CSV file
def createReader(fileName):
    csv_file = open(fileName, newline='')
    reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    return reader  


#writer writes a row [numberOfPeeling,title,line]
def writePeeling(writer, numberOfPeeling,title, line):
    toWrite = []
    toWrite.append(numberOfPeeling)
    toWrite.append(title)
    toWrite[2:] = line
    writer.writerow(toWrite)