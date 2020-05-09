from __future__ import division
import Adafruit_PCA9685
import io
import picamera
import cv2
import numpy
import time
import sys

#sudo service motion stop
#sudo modprobe bcm2835-v4l2

#prende un frame dalla camera e lo ritorna
def captureFrame(camera):

	#crea uno stream in memoria
	stream = io.BytesIO()

	#cattura il frame corrente dalla camera e lo inserisce nello stream in memoria
	camera.capture(stream, format='jpeg')

	#converte lo stream in memoria in un array numpy
	image_arr = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

	#crea una immagine opencv dall'array numpy
	image = cv2.imdecode(image_arr, 1)

	return image;
    
#cattura delle facce sul frame corrente
def faceCapture(frame):    
    global count

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

    #salva l'immagine in un file ed incrementa il count
    cv2.imwrite('frames/frame'+str(count)+'.jpg', frame)
    count+=1

    return ractangle

#get pulse from degree
def map(x):
    degree_min = -90
    degree_max = 90
    pulse_min = 150
    pulse_max = 600
    y = (x - degree_min) * (pulse_max - pulse_min) / (degree_max - degree_min) + pulse_min
    return int(y)

#cerca la faccia
def searchFace(camera):
	for degreeH in [-15, -20, -25, -30, -35]:
	    for degreeW in [-15, 0, 15, -20, 20]:
			#aggiorna la posizione della telecamera
			pwm.set_pwm(hServo, 0, map(degreeH))
			pwm.set_pwm(wServo, 0, map(degreeW))
        
			for i in range(2):
				#cattura un frame dalla camera
				frame = captureFrame(camera)

				#cerca la faccia all'interno del frame
				rectangle = faceCapture(frame)

				if rectangle is not None:
					break;

			#se trova la faccia esce
			if rectangle is not None:
				for i in range(5):
					pwm.set_pwm(hServo, 0, map(degreeH -10))
					time.sleep(0.4)
					pwm.set_pwm(hServo, 0, map(degreeH +10))
					time.sleep(0.4)
				pwm.set_pwm(hServo, 0, map(degreeH))	
				return hServo, wServo, rectangle

#segue la faccia
def followFace(camera, rect, w, h):
	while(True):
			
		#cattura un frame dalla camera
		frame = captureFrame(camera)

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

pwm = Adafruit_PCA9685.PCA9685()
servo_min = 150  # Min pulse length out of 4096
servo_max = 500  # Max pulse length out of 4096

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

#servos
hServo = 0
wServo = 1

#carica i cascade files di training
face_cascades = []
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml'))
face_cascades.append(cv2.CascadeClassifier('lbpcascade/lbpcascade_frontalface.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt2.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt_tree.xml'))
face_cascades.append(cv2.CascadeClassifier('haarcascade/haarcascade_profileface.xml'))
face_cascades.append(cv2.CascadeClassifier('lbpcascade/lbpcascade_profileface.xml'))

#inizializza il count
count = 1

#inizializza la camera
camera = picamera.PiCamera()
camera.resolution = (280, 260)
camera.start_preview()

#ciclo infinito..
while(True):
	searchFace(camera)
	#h, w, rect = searchFace(camera)
	#if rect is not None:
		#followFace(camera, rect, h, w)
		#camera.stop_preview()
	
	#attende
	time.sleep(0.5)		
    

