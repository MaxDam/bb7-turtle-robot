#sudo apt-get update 
#sudo apt-get install gfortran libatlas-base-dev libopenblas-dev liblapack-dev -y
#pip3 install scikit-learn --index-url https://piwheels.org/simple
#pip install csv

#sudo apt-get install libatlas-base-dev
#pip install -U scikit-learn

import numpy as np
import cv2
#import csv

from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def trainClass(name, inputs, class_labels):
    save_file = "train/" +name + ".xml"
    model = cv2.ml.RTrees_create()
    model.setMaxDepth(20)
    #model.setActiveVarCount(0)
    #model.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 128, 1))
    model.train(np.float32(inputs), cv2.ml.ROW_SAMPLE, class_labels.astype(int))
    model.save(save_file)

def predictClass(name, inputs):
    load_file = "train/" +name + ".xml"
    model = cv2.ml.RTrees_load(load_file)
    _, resp = model.predict(np.float32(inputs))
    return resp.ravel()


#test
x_train = np.array([[2.5,3.3,4.5], [5.4,6.2,3.3], [5.4,6.3,7.6]])
y_train = np.array([1, 2, 0])
x_test = np.array([[2.5,3.3,4.5]])
trainClass("test", x_train, y_train)
predict = predictClass("test", x_test)
print(predict)




#return image input histogram (Cumulative Distribution Function)
def getInputHistogram(self):
    hist, _ = np.histogram(self.inputImage.flatten(), self.inputNumber, [0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()
    #return hist
    return cdf_normalized

def getData(self):
    X = self.getInputHistogram()
    Y = [cv2.getTrackbarPos(key, self.windowName) for key in iter(self.trainableParams.keys())]
    return X, Y

#append data to csv
def writeDataToCsv(name, X, Y):
    #csvFileName = "train/" +name + ".csv"
    #with open(csvFileName, mode='a', newline='') as csvFile:
    #    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #    writer.writerow(np.hstack([X, Y]))

    csvFileName = "train/" +name + ".csv"
    data_file = open(csvFileName,"w")
    for 
    data_file.write(",".join(np.hstack([X, Y]).astype(str)))

#train the model
def trainModel(name, numOutput=1):
    print("TRAINING MODEL...")

    #read data, slit and shuffle
    data = []
    csvFileName = "train/" +name + ".csv"
    with open(csvFileName, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            data.append(row)
    np.random.shuffle(data)
    X = data[:,:-numOutput]
    Y = data[:,-numOutput:]
    
    #train model
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    scaler = preprocessing.StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    model = RandomForestRegressor(n_estimators=100, max_depth=30, random_state=0)
    model.fit(X_train, Y_train)
    
    #verify model
    Y_prediction_train = model.predict(X_train)
    rSquareTrain = r2_score(Y_train, Y_prediction_train)
    maeTrain = mean_absolute_error(Y_train, Y_prediction_train)
    rmseTrain = mean_squared_error(Y_train, Y_prediction_train)**0.5
    Y_prediction_test = model.predict(X_test)
    rSquareTest = r2_score(Y_test, Y_prediction_test)
    maeTest = mean_absolute_error(Y_test, Y_prediction_test)
    rmseTest = mean_squared_error(Y_test, Y_prediction_test)**0.5
    print("-------------------------------")
    print("MAE-TRAIN: ", maeTrain, " (→ 0)")
    print("MAE-TEST: ", maeTest, " (→ 0)")
    print("-------------------------------")
    print("RMSE-TRAIN: ", rmseTrain, " (→ 0)")
    print("RMSE-TEST: ", rmseTest, " (→ 0)")
    print("-------------------------------")
    print("R^2-TRAIN: ", rSquareTrain, " (→ 1)")
    print("R^2-TEST: ", rSquareTest, " (→ 1)")
    print("-------------------------------")

#predict trainableParams
def predictParams(self, showtrainableParams=False):
    if self.model is not None:
        x = self.getInputHistogram()
        X = self.scaler.transform([x])
        predict = self.model.predict(X)
        predictIndex = 0
        for key in iter(self.trainableParams.keys()):
            self.trainableParams[key] = int(predict[0][predictIndex])
            predictIndex += 1
        if showtrainableParams:
            print(predict)