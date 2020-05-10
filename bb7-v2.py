import jointdriver as jd
import argparse
import time
import random
import io
import picamera
import cv2
import numpy
import time
import sys
import numpy as np
import imutils

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-cmd", "--command", default=0, help="command")

args = ap.parse_args()

#carica i cascade files di training
face_cascades = []
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml'))
face_cascades.append(cv2.CascadeClassifier('lbpcascade/lbpcascade_frontalface.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt2.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt_tree.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_profileface.xml'))
face_cascades.append(cv2.CascadeClassifier('lbpcascade/lbpcascade_profileface.xml'))

#color thresholds (green)
#colorLower = (29, 86, 6)
#colorUpper = (64, 255, 255)
#colorLower = (0, 142, 245)
#colorUpper = (70, 255, 255)
colorLower = np.array([5, 50, 50],np.uint8)
colorUpper = np.array([15, 255, 255],np.uint8)

#inizializza la camera
camera = picamera.PiCamera()
camera.resolution = (280, 260)
camera.start_preview()

#robot happy
def happy():
    #si abbassa in avanti e guarda in su
    jd.moveJoint(jd.RIGHT_BACK_ARM, 60)
    jd.moveJoint(jd.LEFT_BACK_ARM, 60)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, 0)
    jd.moveJoint(jd.LEFT_FRONT_ARM, 0)
    jd.moveJoint(jd.HEAD, 10)
    time.sleep(0.4)

    #nuove il dietro come un cane
    for degree in [30, -30, 30, -30, 30, -30, 30, -30, 0]:
        jd.moveJoint(jd.RIGHT_BACK_SHOULDER, -degree)
        jd.moveJoint(jd.LEFT_BACK_SHOULDER, degree)
        time.sleep(0.2)

#prende un frame dalla camera e lo ritorna
def captureFrame():
    #crea uno stream in memoria
    stream = io.BytesIO()
    #cattura il frame corrente dalla camera e lo inserisce nello stream in memoria
    camera.capture(stream, format='jpeg')
    #converte lo stream in memoria in un array numpy
    image_arr = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
    #crea una immagine opencv dall'array numpy
    image = cv2.imdecode(image_arr, 1)
    #torna l'immagine ctturata
    return image;

#search face
def searchFace():
    #cattura un frame dalla camera
    frame = captureFrame()
    #cerca la faccia all'interno del frame
    rectangle = faceCapture(frame)

    #se trova la faccia..
    if rectangle is not None:        
        print("found face %s" % (str(rectangle)))
    else:
        print("no faces found")

        '''
        #annuisce con la testa
        for _ in range(5):
            jd.moveJoint(jd.HEAD, degreeH -10)
            time.sleep(0.4)
            jd.moveJoint(jd.HEAD, degreeH +10)
            time.sleep(0.4)
        jd.moveJoint(jd.HEAD, degreeH)

        #torna il rettangolo trovato
        return rectangle
        '''

#search ball
def searchBall():
    frame = captureFrame()
    frame = imutils.resize(frame, width=600)
    frame = cv2.resize(frame, (640,480))
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #blurred = cv2.GaussianBlur(frame, (5,5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    #trova i contorni
    contours  = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#[-2]
    contours  = imutils.grab_contours(contours)
    center = None
    
    '''
    for contour in contours:
        area = cv2.contourArea(contour)
        (x, y, w, h) = cv2.boundingRect(contour)
        if  (area < 50 or area > 5000): continue   
        if  h < w * 1.1 or h > w * 3 or (w*h)>2000 : continue  
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  
        print("ball found %s %s %s %s" % (x, y, w, h))
    '''
    #se ha trovato contorni..
    if len(contours) > 0:
        #ottiene il contorno
        c = max(contours , key=cv2.contourArea)
        
        #ottiene il cerchio ed il centro
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        #se il raggio e' maggiore della soglia minima..
        if radius > 10:
            print("ball found %s %s %s %s" % (x, y, radius, str(center)))
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    #salva l'immagine in un file
    cv2.imwrite('frames/'+time.strftime("%Y%m%d-%H%M%S")+'_mask.jpg', mask)
    cv2.imwrite('frames/'+time.strftime("%Y%m%d-%H%M%S")+'.jpg', frame)        


#cattura delle facce sul frame corrente
def faceCapture(frame):    
    ractangle = None
    #converte in scala di grigi
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cerca tramite knn(5) delle facce nel frame corrente
    for face_cascade in face_cascades:
    	faces = face_cascade.detectMultiScale(frameGray, 1.2, 3)
    	#faces = face_cascade.detectMultiScale(frameGray, 1.3, 5)
    	if len(faces) > 0:
    		break;
    
    #messaggio all'utente
    print("Found " + str(len(faces)) + " face(s)")

    #disegna il rettangolo intorno alla faccia individuata
    for (x,y,w,h) in faces:
        ractangle = [x, y, x+w, y+h]
        cv2.rectangle(frame, (x,y),(x+w,y+h), (255,255,0), 2)

    #salva l'immagine in un file
    cv2.imwrite('frames/'+time.strftime("%Y%m%d-%H%M%S")+'.jpg', frame)

    return ractangle

#segue la faccia
def followFace(rect, w, h):
	while(True):
			
		#cattura un frame dalla camera
		frame = captureFrame()

		#cerca la faccia all'interno del frame
		rectangle = faceCapture(frame)
			
		if rectangle is not None:
			if(rectangle[0] > rect[0]):
				pwm.set_pwm(wServo, 0, map(w + 1))
			if(rectangle[0] > rect[0]):
				pwm.set_pwm(wServo, 0, map(w - 1))
			if(rectangle[1] > rect[1]):
				pwm.set_pwm(hServo, 0, map(h + 1))
			if(rectangle[1] > rect[1]):
				pwm.set_pwm(hServo, 0, map(h - 1))
			rect = rectangle
	
		#attende
		time.sleep(0.05)	
        
#posizione iniziale
if(args.command == "standup"):
    jd.zero(50)
    time.sleep(4)
    jd.relax()

#steps
if(args.command == "steps"):
    jd.stepForward(2)
    time.sleep(1)
    jd.stepBack(2)
    time.sleep(1)
    jd.stepTurnLeft(2)
    time.sleep(1)
    jd.stepTurnRight(2)
    time.sleep(1)
    jd.zero(50)
    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

if(args.command == "search"):
    arm_zero_pos=50
    offset_neck=0
    jd.zero(arm_zero_pos)
    time.sleep(1)

    for i in range(4):

        #sceglie la posizione del corpo da assumere in maniera random
        bodyPosition = random.choice(["back-left-weight", "front-right-weight", "back-right-weight", "front-left-weight"])

        #back-left-weight
        if(bodyPosition=="back-left-weight"):
            jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
            jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
            jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-50)
            jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos-70)
            offset_neck = 10

        #front-right-weight
        if(bodyPosition=="front-right-weight"):
            jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-70)
            jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-50)
            jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
            jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
            offset_neck = -10

        #back-right-weight
        if(bodyPosition=="back-right-weight"):
            jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
            jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
            jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-70)
            jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos-50)
            offset_neck = 10

        #back-right-weight
        if(bodyPosition=="front-left-weight"):
            jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-50)
            jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-70)
            jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
            jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
            offset_neck = -10
        
        #muove la testa alla ricerca di un volto
        for degreeH in [-15, -20, -25, -30, -35]:
            for degreeW in [-15, 0, 15, -20, 20]:
                #aggiorna la posizione della testa (telecamera)
                jd.moveJoint(jd.HEAD, degreeH)
                jd.moveJoint(jd.NECK, degreeW)

                #cerca una faccia
                searchFace()

    time.sleep(1)
    jd.zero(arm_zero_pos)
    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

#cameratest
if(args.command == "cameratest"):
    jd.zero(50)
    jd.moveJoint(jd.HEAD, -20)
    time.sleep(1)
    for i in range(20):
        print("step %s" % i)
        searchFace()
        #searchBall()
        time.sleep(0.1)

    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

#scan head
if(args.command == "scan"):
    jd.zero(50)
    jd.headScanning(0.3)

#pulitura
if(args.command == "relax"):
    jd.relax()
