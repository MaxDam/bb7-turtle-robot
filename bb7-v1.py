import jointdriver as jd
import argparse
import time

#parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-cmd", "--command", default=0, help="command")

args = ap.parse_args()


def exercise1(joint):
	jd.moveJoint(joint, 0)
	time.sleep(0.3)
	for degree in [30, 0, 30, 0, 30, 0]:
		jd.moveJoint(joint, degree)
		time.sleep(0.2)
	time.sleep(0.5)
	for degree in [-30, 0, -30, 0, -30, 0]:
		jd.moveJoint(joint, degree)
		time.sleep(0.2)
	time.sleep(0.5)	

#posizione iniziale
if(args.command == "standup"):
    jd.zero(50)
    time.sleep(4)
    jd.relax()

if(args.command == "standup2"):
    jd.zero(50)
    time.sleep(4)
    jd.moveJoint(jd.RIGHT_BACK_ARM, 0)
    jd.moveJoint(jd.LEFT_BACK_ARM, -20)
    time.sleep(1)
    for degree_arm, degree_schoulder in zip([-40, -40, 40, 40], [0, 40, 40, 0]):
        jd.moveJoint(jd.RIGHT_FRONT_ARM, degree_arm)
        time.sleep(0.2)
        jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, degree_schoulder)
        time.sleep(0.2)
    time.sleep(4)
    jd.zero()
    time.sleep(0.2)
    jd.relax()

'''
if(args.command.startswith("move")):
    movements = args.command.split(":")[1]
    for m in movements.split(","):
        if(m[0:1]=="H"):
            jd.moveJoint(jd.HEAD, int(m[1:]))
        if(m[0:1]=="N"):
            jd.moveJoint(jd.NECK, int(m[1:]))
        if(m[0:3]=="RFA"):
            jd.moveJoint(jd.RIGHT_FRONT_ARM, int(m[3:]))
        if(m[0:3]=="LFA"):
            jd.moveJoint(jd.LEFT_FRONT_ARM, int(m[3:]))
        if(m[0:3]=="RBA"):
            jd.moveJoint(jd.RIGHT_BACK_ARM, int(m[3:]))
        if(m[0:3]=="LBA"):
            jd.moveJoint(jd.LEFT_BACK_ARM, int(m[3:]))
        if(m[0:3]=="RFS"):
            jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, int(m[3:]))
        if(m[0:3]=="LFS"):
            jd.moveJoint(jd.LEFT_FRONT_ARM, int(m[3:]))
        if(m[0:3]=="RBS"):
            jd.moveJoint(jd.RIGHT_BACK_SHOULDER, int(m[3:]))
        if(m[0:3]=="LBS"):
            jd.moveJoint(jd.LEFT_BACK_SHOULDER, int(m[3:]))
'''

#esercizio1
if(args.command == "exercise"):
    jd.standup()
    time.sleep(0.5)
    exercise1(jd.HEAD)
    exercise1(jd.NECK)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, 0)
    exercise1(jd.RIGHT_FRONT_SHOULDER)
    exercise1(jd.RIGHT_FRONT_ARM)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, 60)
    jd.moveJoint(jd.LEFT_FRONT_ARM, 0)
    exercise1(jd.LEFT_FRONT_SHOULDER)
    exercise1(jd.LEFT_FRONT_ARM)
    jd.moveJoint(jd.LEFT_FRONT_ARM, 60)
    jd.moveJoint(jd.RIGHT_BACK_ARM, 0)
    exercise1(jd.RIGHT_BACK_SHOULDER)
    exercise1(jd.RIGHT_BACK_ARM)
    jd.moveJoint(jd.RIGHT_BACK_ARM, 60)
    jd.moveJoint(jd.LEFT_BACK_ARM, 0)
    exercise1(jd.LEFT_BACK_SHOULDER)
    exercise1(jd.LEFT_BACK_ARM)
    jd.moveJoint(jd.LEFT_BACK_ARM, 60)
    time.sleep(0.5)
    jd.relax()

#happy
if(args.command == "happy"):
    jd.zero()
    time.sleep(2)
    jd.zero(30)

    for i in range(4):
        jd.moveJoint(jd.RIGHT_BACK_ARM, 0)
        jd.moveJoint(jd.LEFT_BACK_ARM, 0)
        jd.moveJoint(jd.RIGHT_FRONT_ARM, 60)
        jd.moveJoint(jd.LEFT_FRONT_ARM, 60)
        jd.moveJoint(jd.HEAD, 10)
        time.sleep(0.4)
        jd.moveJoint(jd.RIGHT_BACK_ARM, 60)
        jd.moveJoint(jd.LEFT_BACK_ARM, 60)
        jd.moveJoint(jd.RIGHT_FRONT_ARM, 0)
        jd.moveJoint(jd.LEFT_FRONT_ARM, 0)
        jd.moveJoint(jd.HEAD, -10)
        time.sleep(0.4)
    jd.zero(30)

    jd.moveJoint(jd.RIGHT_BACK_ARM, -10)
    jd.moveJoint(jd.LEFT_BACK_ARM, -10)
    for degree in [10, -10, 10, -10, 10, -10, 10, -10, 0]:
        jd.moveJoint(jd.HEAD, degree)
        jd.moveJoint(jd.RIGHT_BACK_SHOULDER, -5*degree)
        jd.moveJoint(jd.LEFT_BACK_SHOULDER, 5*degree)
        time.sleep(0.2)
    
    jd.zero()
    time.sleep(1)
    jd.relax()

#step
if(args.command == "step"):
    shoulder_range = 40
    arm_range = 40
    arm_zero_pos = 50
    delay=0.1

    jd.zero(arm_zero_pos)
    time.sleep(delay)
    for i in range(4):
        #abbassa il retro
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-50)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos-70)
        time.sleep(delay)
        #muove a gamba anteriore per il passo
        jd.moveJoint(jd.RIGHT_FRONT_ARM, -40)
        time.sleep(delay)
        jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, 40)
        jd.moveJoint(jd.NECK, 40)
        time.sleep(delay)
        #reimposta l'assetto gambe
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.NECK, -40)
        time.sleep(delay)
        #abbassa il davanti
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-90)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-20)
        time.sleep(delay)
        #muove a gamba posteriore per il passo
        jd.moveJoint(jd.LEFT_BACK_ARM, -40)
        time.sleep(delay)
        jd.moveJoint(jd.LEFT_BACK_SHOULDER, 40)
        jd.moveJoint(jd.NECK, 0)
        time.sleep(delay)
        #reimposta l'assetto gambe
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.NECK, -30)
        time.sleep(delay)
        #effettua la spinta per il passo
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, 0)
        jd.moveJoint(jd.LEFT_FRONT_SHOULDER, -40)
        jd.moveJoint(jd.LEFT_BACK_SHOULDER, 0)
        jd.moveJoint(jd.RIGHT_BACK_SHOULDER, -40)
        jd.moveJoint(jd.NECK, 40)
        time.sleep(delay)

        #abbassa il retro
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-70)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos-50)
        time.sleep(delay)
        #muove a gamba anteriore per il passo
        jd.moveJoint(jd.LEFT_FRONT_ARM, -40)
        time.sleep(delay)
        jd.moveJoint(jd.LEFT_FRONT_SHOULDER, 40)
        time.sleep(delay)
        #reimposta l'assetto gambe
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
        time.sleep(delay)
        #abbassa il davanti
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-50)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-70)
        time.sleep(delay)
        #muove a gamba posteriore per il passo
        jd.moveJoint(jd.RIGHT_BACK_ARM, -40)
        time.sleep(delay)
        jd.moveJoint(jd.RIGHT_BACK_SHOULDER, 40)
        time.sleep(delay)
        #reimposta l'assetto gambe
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
        time.sleep(delay)
        #effettua la spinta per il passo
        jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
        jd.moveJoint(jd.RIGHT_FRONT_SHOULDER, -40)
        jd.moveJoint(jd.LEFT_FRONT_SHOULDER, 0)
        jd.moveJoint(jd.LEFT_BACK_SHOULDER, -40)
        jd.moveJoint(jd.RIGHT_BACK_SHOULDER, 0)
        time.sleep(delay)

    jd.zero(arm_zero_pos)
    time.sleep(2)
    jd.zero()
    time.sleep(0.3)
    jd.relax()

if(args.command == "shiftweight"):
    arm_zero_pos=50
    jd.zero(arm_zero_pos)
    time.sleep(1)
    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-50)
    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos-70)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
    jd.moveJoint(jd.NECK, 40)
    jd.moveJoint(jd.HEAD, -20)
    time.sleep(1)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-70)
    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-50)
    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
    jd.moveJoint(jd.NECK, -30)
    jd.moveJoint(jd.HEAD, 30)
    time.sleep(1)
    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos-70)
    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos-50)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos)
    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos)
    jd.moveJoint(jd.NECK, 50)
    jd.moveJoint(jd.HEAD, -10)
    time.sleep(1)
    jd.moveJoint(jd.RIGHT_FRONT_ARM, arm_zero_pos-50)
    jd.moveJoint(jd.LEFT_FRONT_ARM, arm_zero_pos-70)
    jd.moveJoint(jd.RIGHT_BACK_ARM, arm_zero_pos)
    jd.moveJoint(jd.LEFT_BACK_ARM, arm_zero_pos)
    jd.moveJoint(jd.NECK, 10)
    jd.moveJoint(jd.HEAD, -30)
    time.sleep(1)
    jd.zero(arm_zero_pos)
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
