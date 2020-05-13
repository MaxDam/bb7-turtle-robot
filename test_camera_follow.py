from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import numpy as np
import jointdriver as jd

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 220):
        panAngle += 10
		#if panAngle > 140: panAngle = 140
		if panAngle > 40: panAngle = 40
		jd.moveJoint(jd.NECK, panAngle)
 
    if (x > 280):
        panAngle -= 10
        if panAngle < 40: panAngle = 40
        jd.moveJoint(jd.NECK, panAngle)

    if (y < 160):
        tiltAngle += 10
        if tiltAngle > 140: tiltAngle = 140
		if tiltAngle > 40: tiltAngle = 40
        jd.moveJoint(jd.HEAD, tiltAngle)
 
    if (y > 210):
        tiltAngle -= 10
        if tiltAngle < 40: tiltAngle = 40
        jd.moveJoint(jd.HEAD, tiltAngle)

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
vs = VideoStream(0).start()
time.sleep(2.0)

# Initialize angle servos at 90-90 position
global panAngle
global tiltAngle
#panAngle = 90
#tiltAngle =90
panAngle = 0
tiltAngle =0

# positioning Pan/Tilt servos at initial position
jd.moveJoint(jd.NECK, panAngle)
jd.moveJoint(jd.HEAD, tiltAngle)

# loop over the frames from the video stream
while True:
	# grab the next frame from the video stream, Invert 180o, resize the
	# frame, and convert it to the HSV color space
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	frame = imutils.rotate(frame, angle=180)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the object color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	#mask = cv2.inRange(hsv, (24, 100, 100), (44, 255, 255))
	mask = cv2.inRange(hsv, np.array([13, 0, 255]), np.array([50, 255, 255]))
	mask |= cv2.inRange(hsv, np.array([(0, 185, 181)]), np.array([19, 247, 246]))

	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			# position Servo at center of circle
			mapServoPosition(int(x), int(y))

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	
	# if [ESC] key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
            break

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
jd.moveJoint(jd.NECK, 90)
jd.moveJoint(jd.HEAD, 90)
cv2.destroyAllWindows()
vs.stop()
