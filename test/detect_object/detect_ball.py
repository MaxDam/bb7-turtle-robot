import argparse
import cv2
import imutils
import numpy as np

#initialize capture (video or camera)
camera = cv2.VideoCapture(0)
camera.set(3, 320)
camera.set(4, 240)

def printRangeCenterColor(frame, interval):
    minH, minS, minV = 255, 255, 255
    maxH, maxS, maxV = 0, 0, 0
    w, h = 320, 240
    centerX, centerY = w//2, h//2
    for x in range(centerX-interval, centerX+interval):
        for y in range(centerY-interval, centerY+interval):
            h, s, v = frame[x,y]
            if h < minH: minH = h
            if s < minS: minS = s
            if v < minV: minV =v
            if h > maxH: maxH = h
            if s > maxS: maxS = s
            if v > maxV: maxV = v
    print("center color range (%s, %s, %s), (%s, %s, %s)" % (minH, minS, minV, maxH, maxS, maxV))
    cv2.line(frame, (centerX-interval, centerY), (centerX+interval, centerY), (0, 255, 0), thickness=2)
    cv2.line(frame, (centerX, centerY-interval), (centerX, centerY+interval), (0, 255, 0), thickness=2)
    return ((minH, minS, minV), (maxH, maxS, maxV))    

#color thresholds
'''
colorThresholds = (
    ( (13,  0,   255), (50,  255, 255) ), #orangeDay
    ( (0,   185, 181), (19,  247, 246) ), #orangeNight
    ( (61,  91,  133), (85,  255, 255) ), #greenDay
    ( (70,  156, 64),  (87,  255, 255) ), #greenNight
    #( (97,  115, 136), (121, 250, 255) ), #blueDay
    #( (107, 153, 127), (123, 255, 242) )  #blueNight
)
'''
colorThresholds = (
    ( (10,  150,   150), (30,  255, 255) ), #orange day
    ( (40,  100,   150), (90,  255, 255) ), #green day
    #( (10,  150,   100), (30,  255, 255) ), #orange night
    #( (40,  100,   0), (90,  255, 150) ), #green night
)

#infinite loop
while True:
    #Capture frame-by-frame
    ret, frame = camera.read()
    if frame is None: break

    #printRangeCenterColor(frame, 10)

    blurred = frame #cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #applica i range di colori
    mask = None
    for minColor, maxColor in colorThresholds:
        #minColor = np.asarray(minColor, dtype=np.float32)
        #maxColor = np.asarray(maxColor, dtype=np.float32)
        if mask is None:
             mask = cv2.inRange(hsv, minColor, maxColor)
        else:
            mask |= cv2.inRange(hsv, minColor, maxColor)
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    #trova i contorni
    contours  = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    maxRadius = 8
    maxCenter = (0,0)
    for contour in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        print("radius %s" % radius)   
        '''
        if radius > 8:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        '''
        if radius > maxRadius:
            maxRadius = radius
            maxCenter = center

    if len(contours) > 0:
        cv2.circle(frame, maxCenter, int(maxRadius), (0, 255, 255), 2)
        cv2.circle(frame, maxCenter, 5, (0, 0, 255), -1)
    
    #view video to the screen
    cv2.imshow('Mask', mask)
    cv2.imshow('Video', frame)
    
    #if the 'q' key is pressed, stop the loop
    if cv2.waitKey(35) & 0xFF == ord('q'):
       break

#When everything is done, release the capture
camera.release()
cv2.destroyAllWindows()