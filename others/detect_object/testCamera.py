import numpy as np
import cv2

vc = cv2.VideoCapture(0)
 
while(True):
    ret, frame = vc.read()
    frame = cv2.flip(frame, -1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vc.release()
cv2.destroyAllWindows()
