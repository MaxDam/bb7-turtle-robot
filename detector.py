
import cv2
from math import sin, cos, radians
import jointdriver as jd
import time
import random
import io
import picamera
import numpy as np
import math

#inizializza la camera
camera = picamera.PiCamera()
#camera.resolution = (280, 260)
camera.resolution = (320, 240)
#camera.resolution = (640, 480)
camera.start_preview()

#carica il cascade file
face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_alt2.xml")
#face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

#color thresholds
colorThresholds = (
    ( (13,  0,   255), (20,  255, 255) ), #orangeDay
    ( (0,   185, 181), (19,  247, 246) ), #orangeNight
    ( (61,  91,  133), (85,  255, 255) ), #greenDay
    ( (70,  156, 64),  (87,  255, 255) ), #greenNight
    ( (97,  115, 136), (121, 250, 255) ), #blueDay
    ( (107, 153, 127), (123, 255, 242) )  #blueNight
)
MIN_RADIUS_THRWSHOLD = 10

#settaggi del face detection
faceDetectionSettings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 3, 
    'minSize': (50, 50)
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

#prende un frame dalla camera e lo ritorna
def captureFrame():
    #crea uno stream in memoria
    stream = io.BytesIO()
    #cattura il frame corrente dalla camera e lo inserisce nello stream in memoria
    camera.capture(stream, format='jpeg')
    #converte lo stream in memoria in un array numpy
    image_arr = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #crea una immagine opencv dall'array numpy
    image = cv2.imdecode(image_arr, 1)
    #torna l'immagine ctturata
    return image;

#detect ball
def detectBall(debug=False):
    detected = None

    frame = captureFrame()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #applica i range di colori
    mask = None
    for ct in colorThresholds:
        minColor, maxColor = ct
        if mask is None:
             mask = cv2.inRange(hsv, minColor,  maxColor)
        else:
            mask |= cv2.inRange(hsv, minColor,  maxColor)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    #print center color
    if(debug):
        printRangeCenterColor(frame, 10)
        
    #trova i contorni
    contours  = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    #scorre i contorni trovati
    for contour in contours:
        #ottiene il cerchio ed il centro
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #print("radius %s" % radius)   
            
        #se il raggio supera la soglia minima..
        if radius > MIN_RADIUS_THRWSHOLD:
            if(debug): 
                print("ball found %s %s" % (radius, str(center)))
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

            #torna il cerchio trovato
            detected = (center, radius)
            break
    
    #salva l'immagine in un file
    if(debug): 
        cv2.imwrite('frames/'+time.strftime("%Y%m%d-%H%M%S")+'.mask.jpg', mask)
        cv2.imwrite('frames/'+time.strftime("%Y%m%d-%H%M%S")+'.jpg', frame)     

    #torna il cerchio trovato
    return detected 


#stampa il range di colori nella posizione centrale della immagine
def printRangeCenterColor(frame, interval):
    minH, minS, minV = math.inf, math.inf, math.inf
    maxH, maxS, maxV = 0,0,0
    w, h = camera.resolution
    for x in range(w//2-interval, w//2+interval):
        for y in range(h//2-interval, h//2+interval):
            h, s, v = frame[x,y]
            if h < minH: minH = h
            if s < minS: minS = s
            if v < minV: minV =v
            if h > maxH: maxH = h
            if s > maxS: maxS = s
            if v > maxV: maxV = v
    print("center color range (%s, %s, %s), (%s, %s, %s)" % (minH, minS, minV, maxH, maxS, maxV))
    cv2.line(frame, (w//2-interval, h//2-interval), (w//2+interval, h//2+interval), (0, 255, 0), thickness=2)
    return ((minH, minS, minV), (maxH, maxS, maxV))    
    

#segue la palla
def followBall(neckDegree, headDegree, debug=False):
        
    MAX_NECK_DEGREE = 35
    MIN_NECK_DEGREE = -35
    MAX_HEAD_DEGREE = 35
    MIN_HEAD_DEGREE = -35
    DEGREE_STEP_SIZE = 2
    PIXEL_THRESHOLD = 10
    center = None

    #cerca la palla all'interno del frame, e se la trova..
    detected = detectBall()
    if detected is not None:
        center, _ = detected

        #ottiene le coordinate della camera
        w, h = camera.resolution
        w_diff = center[0] - w//2
        h_diff = center[1] - h//2

        #decide in quale direzione andare
        if(w_diff > PIXEL_THRESHOLD):
            neckDegree += DEGREE_STEP_SIZE
            print("- collo a destra %s" % (w_diff))        
        if(w_diff < -PIXEL_THRESHOLD):
            neckDegree -= DEGREE_STEP_SIZE
            print("- collo a sinstra %s" % (w_diff))
        if(h_diff > PIXEL_THRESHOLD):
            headDegree += DEGREE_STEP_SIZE
            print("- testa su %s" % (h_diff))
        if(h_diff < -PIXEL_THRESHOLD):
            headDegree -= DEGREE_STEP_SIZE
            print("- testa giu %s" % (h_diff))

        #limita entro un range i movimenti
        neckDegree = max( min(neckDegree, MAX_NECK_DEGREE), MIN_NECK_DEGREE )
        headDegree = max( min(headDegree, MAX_HEAD_DEGREE), MIN_HEAD_DEGREE )

        #muove la testa
        jd.moveJoint(jd.NECK, neckDegree)
        jd.moveJoint(jd.HEAD, headDegree)

    #torna le nuove coordinate
    return center, neckDegree, headDegree

#detect face
def detectFace(debug=False):
    detected = None

    #cattura un frame dalla camera
    frame = captureFrame()

    #converte in scala di grigi
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #gira l'immagine nelle diverse angolazioni
    for angle in [0, -25, 25]:
        frameRotated = rotate_image(frameGray, angle)

        #effettua il detect dell'immagine
        detected = face_cascade.detectMultiScale(frameRotated, **faceDetectionSettings)
        if len(detected):
            #se ha trovato qualcosa ottiene il rettangolo riportandolo dopo avere ruotato al contrario le coordinate
            detected = [rotate_point(detected[-1], frameGray, -angle)]
            break
    
    if(debug):
        if detected is not None:
            print("face found %s" % str(detected))
        #visualizza sull'immagine i rettangoli trovati
        for x, y, w, h in detected[-1:]:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
        #salva l'immagine in un file
        cv2.imwrite('frames/'+time.strftime("%Y%m%d-%H%M%S")+'.jpg', frame)

    #torna il rettangolo trovato
    return detected


#segue la faccia
def followFace(prevRect, w, h):
        
    #cerca la faccia all'interno del frame
    detected = detectFace()
        
    if detected is not None:
        if(detected[0] > prevRect[0]):
            jd.moveJoint(jd.HEAD, w + 1)
        if(detected[0] > prevRect[0]):
            jd.moveJoint(jd.HEAD, w - 1)
        if(detected[1] > prevRect[1]):
            jd.moveJoint(jd.NECK, h + 1)
        if(detected[1] > prevRect[1]):
            jd.moveJoint(jd.NECK, h - 1)

    return detected
