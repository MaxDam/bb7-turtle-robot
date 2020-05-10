import argparse
import cv2
from parameters import Parameters
import numpy as np

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--train", default=True, action="store_true", help="train")
ap.add_argument("-v", "--video", default=0, help="video file path")
ap.add_argument("-p", "--predict", default=False, action="store_true", help="predict")
args = ap.parse_args()

#set parameters
p = Parameters('video', train=args.train)
p.add('Erode', 1, 6)
p.add('Dilate', 4, 6)
p.add('Gamma', 5, 10, trainable=False)
p.add('Inverse', 0, 1, trainable=False)
p.addHSV('Lower', (29, 86, 6))
p.addHSV('Upper', (64, 255, 255))

#adjust contrast and brightness input image
def adjustContrastBrightness(image, gamma=1.0):
    if gamma == 0: gamma = 0.01
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i/255.0, 1.0/gamma)*255.0, 0, 255)
    return cv2.LUT(image, lookUpTable)

#initialize capture (video or camera)
video_capture = cv2.VideoCapture(args.video)

#if we are in predict mode, first at all execute training
if args.predict:
    p.trainModel()

#infinite loop
while True:

    #Capture frame-by-frame and set input
    ret, frame = video_capture.read()
    #frame = adjustContrastBrightness(frame, gamma=(int(p.get('Gamma'))/5))
    p.setInput(frame)
    
    #get a prediction
    if args.predict:
        p.predictParams(True)

    #resize the frame
    image = cv2.resize(frame, (640, 360))

    #apply blur
    image = cv2.GaussianBlur(image, (11,11), 0)

    #convert frame to the HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #create mask
    mask = cv2.inRange(hsv, p.getHSV('Lower'), p.getHSV('Upper'))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    if p.get('Inverse') == 1:
        mask = ~mask

    #view video to the screen
    p.showInputFrame()
    cv2.imshow('myvideo', mask)

    #if the 'q' key is pressed, stop the loop
    #if the 's' key is pressed, save the data
    k = cv2.waitKey(30) & 0xff
    if k == ord('q'):
        break
    if k == ord('s'):
        p.saveData()
        print("train data count: " + p.getTrainDataCount())

#stampa i parametri
#p.printParams()

#When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()