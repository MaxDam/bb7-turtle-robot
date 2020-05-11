import argparse
import cv2
import imutils
import numpy as np

#initialize capture (video or camera)
camera = cv2.VideoCapture(0)

#verde
#greenColorLower = (40, 0, 0)
#greenColorUpper = (130, 255, 255) #(80, 255,255) (130, 255, 255)
greenColorLower = (75, 0, 0)
greenColorUpper = (90, 255, 255)
#arancione
orangeColorLower = (0, 165, 165)
orangeColorUpper = (150, 255, 255) #(80, 255,255) (130, 255, 255)

#infinite loop
while True:
    #Capture frame-by-frame
    ret, frame = camera.read()
    if frame is None: break

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, greenColorLower, greenColorUpper)
    mask2 = cv2.inRange(hsv, orangeColorLower, orangeColorUpper)
    mask = mask1 | mask2
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    #trova i contorni
    contours  = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    
    for contour in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #print("radius %s" % radius)   
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    
    #view video to the screen
    cv2.imshow('Mask', mask)
    cv2.imshow('Video', frame)
    
    #if the 'q' key is pressed, stop the loop
    if cv2.waitKey(35) & 0xFF == ord('q'):
       break

#When everything is done, release the capture
camera.release()
cv2.destroyAllWindows()