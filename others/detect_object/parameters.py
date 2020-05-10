import cv2
import numpy as np
import csv

from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd

class Parameters:
    def __init__(self, windowName, train=True, csvFileName="data.csv", inputNumber=10):
        self.windowName = windowName
        self.train = train
        self.trainableParams = {}
        self.params = {}
        self.csvFileName = csvFileName
        self.inputNumber = inputNumber
        self.trainDataCount = 0
        self.model = None
        cv2.namedWindow(self.windowName)

    def setInput(self, inputImage):
        self.inputImage = inputImage

    def showInputFrame(self, shape=(500, 300)):
        input_image_view = cv2.resize(self.inputImage, shape)
        cv2.imshow(self.windowName, input_image_view)

    def on_change(self, value):
        pass

    def add(self, name, defaultValue, maxValue, trainable=True):
        if trainable:
            self.trainableParams[name] = defaultValue
            if self.train: 
                cv2.createTrackbar(name, self.windowName, defaultValue, maxValue, self.on_change)
        else:
            self.params[name] = defaultValue  
            cv2.createTrackbar(name, self.windowName, defaultValue, maxValue, self.on_change)

    def addRGB(self, name, defaultValues=(0,0,0)):
        for i, prefix in enumerate(['R','G','B']):
            self.trainableParams[prefix+"-"+name] = defaultValues[i]
            if self.train:
                cv2.createTrackbar(prefix+"-"+name, self.windowName, defaultValues[i], 255, self.on_change)             

    def addHSV(self, name, defaultValues=(0,0,0)):
        for i, prefix in enumerate(['H','S','V']):
            self.trainableParams[prefix+"-"+name] = defaultValues[i]
            if self.train:
                cv2.createTrackbar(prefix+"-"+name, self.windowName, defaultValues[i], 255, self.on_change)

    def addYCbCr(self, name, defaultValues=(0,0,0)):
        for i, prefix in enumerate(['Y','Cb','Cr']):
            self.trainableParams[prefix+"-"+name] = defaultValues[i]
            if self.train:
                cv2.createTrackbar(prefix+"-"+name, self.windowName, defaultValues[i], 255, self.on_change)

    def get(self, name):
        if self.train:
            return cv2.getTrackbarPos(name, self.windowName) 
        elif name in self.trainableParams:
            return self.trainableParams[name]
        elif name in self.params:
            return cv2.getTrackbarPos(name, self.windowName)
        else:
            print("parameter " + name + " not found")
            return 0

    def getRGB(self, name):
        retValue = list()        
        for _, prefix in enumerate(['R','G','B']):
            key = prefix+"-"+name
            if self.train:
                retValue.append(cv2.getTrackbarPos(key, self.windowName))
            elif key in self.trainableParams:
                retValue.append(self.trainableParams[key])
            else:
                print("parameter " + key + " not found")
                retValue.append(0)
        return tuple(retValue)
      
    def getHSV(self, name):
        retValue = list()        
        for _, prefix in enumerate(['H','S','V']):
            key = prefix+"-"+name
            if self.train:
                retValue.append(cv2.getTrackbarPos(key, self.windowName))
            elif key in self.trainableParams:
                retValue.append(self.trainableParams[key])
            else:
                print("parameter " + key + " not found")
                retValue.append(0)
        return tuple(retValue)

    def getYCbCr(self, name):
        retValue = list()        
        for _, prefix in enumerate(['Y','Cb','Cr']):
            key = prefix+"-"+name
            if self.train:
                retValue.append(cv2.getTrackbarPos(key, self.windowName))
            elif key in self.trainableParams:
                retValue.append(self.trainableParams[key])
            else:
                print("parameter " + key + " not found")
                retValue.append(0)
        return tuple(retValue)

    #print default trainableParams
    def printParams(self):
        print("trainable params:")
        for key, value in iter(self.trainableParams.items()):
            print(key+":"+str(value))
        print("not trainable params:")
        for key, value in iter(self.params.items()):
            print(key+":"+str(value))

    #return image input histogram (Cumulative Distribution Function)
    def getInputHistogram(self):
        hist, _ = np.histogram(self.inputImage.flatten(), self.inputNumber, [0,256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max()/ cdf.max()
        #return hist
        return cdf_normalized

    #return input-ouput data in matrix format (X e Y)
    def getData(self):
        X = self.getInputHistogram()
        Y = [cv2.getTrackbarPos(key, self.windowName) for key in iter(self.trainableParams.keys())]
        return X, Y
        
    #append data to csv
    def writeDataToCsv(self, X, Y):
        with open(self.csvFileName, mode='a', newline='') as targetCsvFile:
            writer = csv.writer(targetCsvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(np.hstack([X, Y]))
            self.trainDataCount += 1

    #return train data count
    def getTrainDataCount(self):
        return str(self.trainDataCount)

    #acquires the image data and saves it on the csv
    def saveData(self):
        X, Y = self.getData()
        self.writeDataToCsv(X, Y)

    #train the model
    def trainModel(self):
        print("TRAINING MODEL...")
        data = pd.read_csv("./data.csv", header=None).values
        np.random.shuffle(data)
        X = data[:,:self.inputNumber]
        Y = data[:,self.inputNumber:]
        
        #train model
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
        self.scaler = preprocessing.StandardScaler()
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        self.model = RandomForestRegressor(n_estimators=100, max_depth=30, random_state=0)
        self.model.fit(X_train, Y_train)
        
        #test model
        Y_prediction = self.model.predict(X_test)
        r_square = r2_score(Y_test, Y_prediction)
        mae = mean_absolute_error(Y_test, Y_prediction)
        rmse = mean_squared_error(Y_test, Y_prediction)**0.5
        print("MAE: ", mae, " (→ 0)")
        print("RMSE: ", rmse, " (→ 0)")
        print("R^2: ", r_square, " (→ 1)")

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

