import numpy as np
import cv2

'''
newcomer = np.random.randint(0,100,(1,2)).astype(np.float32)
plt.scatter(newcomer[:,0],newcomer[:,1],80,'g','o')

knn = cv2.KNearest()
knn.train(trainData,responses)
ret, results, neighbours ,dist = knn.find_nearest(newcomer, 3)

print "result: ", results,"\n"
print "neighbours: ", neighbours,"\n"
print "distance: ", dist

plt.show()
'''

def train(samples, class_labels, save_file='trainer/trainer.xml'):
    model = cv2.ml.RTrees_create()
    model.setMaxDepth(20)
    model.setActiveVarCount(0)
    model.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 128, 1))
    train_data = cv2.ml.TrainData_create(samples=samples, layout=cv2.ml.ROW_SAMPLE, responses=class_labels)
    model.train(trainData=train_data)
    model.save(save_file)

def predict(samples, load_file='trainer/trainer.xml'):
    model = cv2.ml.RTrees_load(load_file)
    _ret, responses = model.predict(samples)
    return responses.ravel()

if __name__ == '__main__':
    #samples      : np.ndarray of type np.float32
    #class_labels :  np.ndarray of type int
    #x_train = np.random.randint(0, 5, (10, 3))
    #y_train  = np.random.randint(0, 4, 3)
    #x_test = np.random.randint(0, 5, (10, 3))
    
    x_train = np.array([[1.5,1.3,4.5], [4,2,6.3], [3.4,2.3,4.6]])
    y_train = np.array([4, 2, 1])
    x_test = np.array([[1.7,0.9,3.4]])
    
    train(x_train, y_train)

    predict = predict(x_test)
    print(predict)