import csv
import pandas as pd

def createCSV(name):
    df = pd.DataFrame(list())
    df.to_csv(name)

def createWriter(fileName):
    csv_file = open(fileName, "w")
    writer = csv.writer(csv_file)
    return writer

def createReader(fileName):
    csv_file = open(fileName, newline='')
    reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    return reader  


def closeFile(fileName):
    fileName.close()

def writePeeling(writer, numberOfPeeling,title, line):
    toWrite = []
    toWrite.append(numberOfPeeling)
    toWrite.append(title)
    toWrite[2:] = line
    writer.writerow(toWrite)