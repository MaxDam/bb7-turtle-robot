import jointdriver as jd
import detector as dt
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

#detectface test
if(args.command == "detectface"):
    jd.zero(50)
    jd.moveJoint(jd.HEAD, -20)
    time.sleep(1)
    for i in range(20):
        print("step %s" % i)
        detected = dt.detectFace()
       
        #stampa il risultato
        if detected is not None:        
            print("found face %s" % (str(detected)))

            '''
            #annuisce con la testa e stoppa il ciclo
            for _ in range(5):
                jd.moveJoint(jd.HEAD, degreeH -10)
                time.sleep(0.4)
                jd.moveJoint(jd.HEAD, degreeH +10)
                time.sleep(0.4)
            jd.moveJoint(jd.HEAD, degreeH)
            break
            '''
        else:
            print("no faces found")       

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

            neckDegree = 0
            headDegree = 0
            ballCenter, _ = detected
            for j in range(10):
                ballCenter, neckDegree, headDegree = dt.followBall(ballCenter, neckDegree, headDegree)
                
                if(ballCenter is None):
                    print("loss ball")
                    break

                time.sleep(0.1)

            '''
            #annuisce con la testa e stoppa il ciclo
            for _ in range(5):
                jd.moveJoint(jd.HEAD, degreeH -10)
                time.sleep(0.4)
                jd.moveJoint(jd.HEAD, degreeH +10)
                time.sleep(0.4)
            jd.moveJoint(jd.HEAD, degreeH)
            break
            '''
        else:
            print("no ball found")       

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
