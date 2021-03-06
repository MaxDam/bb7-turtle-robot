import jointdriver as jd
import detector as dt
import argparse
import time
import random
#import io
#import picamera
#import cv2
#import sys
#import numpy as np
#import imutils

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-cmd", "--command", default=0, help="command")

args = ap.parse_args()

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
    
#posizione iniziale
if(args.command == "standup"):
    arm_zero_pos = 50
    jd.zero(arm_zero_pos)
    time.sleep(0.5)
    for _ in range(50):
        mov = random.choice([0, 15, -15])
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-mov)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos+mov)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-mov)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos+mov)
        jd.moveJoint(jd.HEAD, random.choice([0, 3, -3, 0, 2, -2]))
        jd.moveJoint(jd.NECK, random.choice([0, 4, -4, 0, 2, -2]))
        time.sleep(1)
    
    time.sleep(4)
    jd.relax()

#steps
if(args.command == "steps"):
    #va avanti
    jd.stepForward(2)
    time.sleep(1)
    #va indietro
    jd.stepBack(2)
    time.sleep(1)
    #gira a sinistra
    jd.stepTurnLeft(2)
    time.sleep(1)
    #gira a destra
    jd.stepTurnRight(2)
    time.sleep(1)
    #fine
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

    for _ in range(4):

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
                detected = dt.detectFace(debug=True)

                #se trova la faccia la segue
                if detected is not None:        
                    print("found face %s" % (str(detected)))

                    neckDegree = 0
                    headDegree = 0
                    faceRect = detected[-1:]
                    for _ in range(1000):
                        faceRect, neckDegree, headDegree = dt.followFace(neckDegree, headDegree)
                        
                        if(faceRect is None):
                            print("loss face")
                            break

                        time.sleep(0.1)
                else:
                    print("no face found") 

    time.sleep(1)
    jd.zero(arm_zero_pos)
    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

#detectface test
if(args.command == "detectface"):
    jd.zero(50)
    jd.moveJoint(jd.HEAD, -20)
    time.sleep(1)
    for i in range(20):
        print("step %s" % i)
        detected = dt.detectFace(debug=True)
       
        #stampa il risultato
        if detected is not None:        
            print("found face %s" % (str(detected)))
            
            #annuisce con la testa e stoppa il ciclo
            for _ in range(5):
                jd.moveJoint(jd.HEAD, -10)
                time.sleep(0.4)
                jd.moveJoint(jd.HEAD, +10)
                time.sleep(0.4)
            jd.moveJoint(jd.HEAD, 0)
            break

    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

#follow face
if(args.command == "followface"):
    jd.zero(50)
    time.sleep(1)
    for i in range(20):
        print("step %s" % i)
        detected = dt.detectFace()

        #stampa il risultato
        if detected is not None:        
            print("found face %s" % (str(detected)))

            neckDegree = 0
            headDegree = 0
            faceRect = detected[-1:]
            for _ in range(1000):
                faceRect, neckDegree, headDegree = dt.followFace(neckDegree, headDegree)
                
                if(faceRect is None):
                    print("loss face")
                    break

                time.sleep(0.1)
        else:
            print("no face found")       

        time.sleep(0.1)

    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

#detectball test
if(args.command == "detectball"):
    jd.zero(50)
    jd.moveJoint(jd.HEAD, -20)
    time.sleep(1)
    for i in range(20):
        print("step %s" % i)
        detected = dt.detectBall()

        #stampa il risultato
        if detected is not None:        
            print("found ball %s" % (str(detected)))
            
            #annuisce con la testa e stoppa il ciclo
            for _ in range(5):
                jd.moveJoint(jd.HEAD, -10)
                time.sleep(0.4)
                jd.moveJoint(jd.HEAD, +10)
                time.sleep(0.4)
            jd.moveJoint(jd.HEAD, 0)
            break

    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()


#follow ball
if(args.command == "followball"):
    #detect ball
    arm_zero_pos = 50
    jd.zero(arm_zero_pos)
    time.sleep(1)

    #cicla 20 volte
    for i in range(20):
        print("step %s" % i)
        detected = dt.detectBall()
        
        #se ha tovato la palla..
        if detected is not None:        
            print("found ball %s" % (str(detected)))            
            
            #annuisce con la testa ed esce dal ciclo
            for _ in range(5):
                jd.moveJoint(jd.HEAD, -10)
                time.sleep(0.4)
                jd.moveJoint(jd.HEAD, +10)
                time.sleep(0.4)
            jd.moveJoint(jd.HEAD, 0)
            break

        #si muove leggermente in modo random
        mov = random.choice([0, 15, -15])
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-mov)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos+mov)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-mov)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos+mov)
        jd.moveJoint(jd.HEAD, random.choice([0, 3, -3, 0, 2, -2]))
        jd.moveJoint(jd.NECK, random.choice([0, 4, -4, 0, 2, -2]))
        time.sleep(0.1)


    #follow ball
    neckDegree = 3
    headDegree = -20

    #si muove come un cane che vuole giocare
    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-70)
    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-50)
    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
    jd.moveJoint(jd.NECK, neckDegree)
    jd.moveJoint(jd.HEAD, headDegree)
    time.sleep(0.2)
    for degree in [50, -50, 50, -50, 50, -50, 50, -50, 0]:
        jd.moveJoint(jd.RIGHT_BACK_SHOULDER, -degree)
        jd.moveJoint(jd.LEFT_BACK_SHOULDER, degree)
        time.sleep(0.2)

    #cicla x 20 volte    
    for i in range(20):
        print("step %s" % i)
        detected = dt.detectBall(debug=False)

        #se trova la palla..
        if detected is not None:        
            print("found ball %s" % (str(detected)))

            #cicla per seguire la palla
            ballCenter, _ = detected
            loss_count = 0
            for _ in range(10000):
                ballCenter, neckDegree, headDegree = dt.followBall(neckDegree, headDegree, debug=True)
                
                #se va oltre il range del collo si sposta
                if(headDegree > 30):
                    #se va troppo in basso si sposta in alto
                    jd.moveJoint(jd.HEAD, headDegree-5)
                    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
                    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
                    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
                    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
                if(neckDegree > 30) : 
                    #se va troppo a destra si sposta a destra
                    neckDegree -= 30
                    jd.stepTurnRight(1)
                    jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, 0)
                    jd.moveJoint(jd.LEFT_FRONT_SHOULDER, 0)
                    jd.moveJoint(jd.RIGHT_BACK_SHOULDER, 0)
                    jd.moveJoint(jd.LEFT_BACK_SHOULDER, 0)
                    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-70)
                    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-50)
                    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
                    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
                    jd.moveJoint(jd.NECK, neckDegree)
                    jd.moveJoint(jd.HEAD, headDegree)
                if(neckDegree < -30): 
                    #se va troppo a sinistra si sposta a sinistra
                    neckDegree += 15
                    jd.stepTurnLeft(1)
                    jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, 0)
                    jd.moveJoint(jd.LEFT_FRONT_SHOULDER, 0)
                    jd.moveJoint(jd.RIGHT_BACK_SHOULDER, 0)
                    jd.moveJoint(jd.LEFT_BACK_SHOULDER, 0)  
                    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-70)
                    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-50)
                    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
                    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
                    jd.moveJoint(jd.NECK, neckDegree)
                    jd.moveJoint(jd.HEAD, headDegree)
                    
                #se perde la palla incrementa il loss count
                if(ballCenter is None):
                    print("loss ball")
                    loss_count += 1
                else:
                    loss_count = 0

                #se ha perso la palla piu' di 20 volte esce dal ciclo
                if(loss_count > 20):
                    break;

                #time.sleep(0.1)    
        else:
            print("no ball found")       

        time.sleep(0.1)

    #fine
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

#stop della camera
dt.stop()