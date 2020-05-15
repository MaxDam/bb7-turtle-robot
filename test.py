import numpy as np
import os

name = "test"

def writeDataToCsv(name, X, Y): 
    csvFileName = "train/" +name + ".csv"
    with open(csvFileName, mode='a', newline='') as csvFile:
        row = np.hstack([X, Y])
        csvFile.write(",".join(row.astype(str)) + os.linesep)

writeDataToCsv(name, [10,12,14], 1)
writeDataToCsv(name, [13,52,24], 0)
writeDataToCsv(name, [92,42,14], 3)

data = []
csvFileName = "train/" +name + ".csv"
with open(csvFileName, 'r') as csvFile:
    for row in csvFile:
        row = row.replace(os.linesep, '')
        data.append(row.split(","))

#print(data)
numOutput = 1
data = np.array(data)
np.random.shuffle(data)
X = data[:,:-numOutput]
Y = data[:,-numOutput:]
print(X)
print("__")
print(Y)