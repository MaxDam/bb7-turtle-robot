import io
import picamera
import cv2
import numpy
import time

#prende un frame dalla camera e lo ritorna
def captureFrameFromCamera():

    #crea uno stream in memoria
    stream = io.BytesIO()

    with picamera.PiCamera() as camera:	
        #inizializza la risoluzione della camera
        camera.resolution = (320, 240)
        #camera.resolution = (800, 600)

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

    ractangle = ()
	
    #converte in scala di grigi
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cerca tramite knn(5) delle facce nel frame corrente
    faces = face_cascade.detectMultiScale(frameGray, 1.1, 5)
    #faces += face_cascade2.detectMultiScale(frameGray, 1.1, 5)

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

#carica i cascade files di training
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml')
#face_cascade2 = cv2.CascadeClassifier('haarcascade/haarcascade_profileface.xml')

#inizializza il count
count = 1

#ciclo infinito..
while(True):
    #print("scan frame to capture face")

    #cattura un frame dalla camera
    frame = captureFrameFromCamera()

    #cerca la faccia all'interno del frame
    faceCapture(frame)

    #attende 1 secondo
    time.sleep(0.1)

