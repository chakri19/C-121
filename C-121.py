import cv2
import time
import numpy as np
from numpy.lib.type_check import _imag_dispatcher

fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,480))

#opening up web cam
cap = cv2.VideoCapture(0)

#making code sleep for 2 secs
time.sleep(2)
bg = 0

for x in range(60):
    #ret refers to boolean values, bg stores the feed
    ret, bg = cap.read()

#flipping image horizontally
bg = np.flip(bg, axis = 1)

while (cap.isOpened()):
    frame, _imag_dispatcher = cap.read()
    if not ret:
        break
    frame = np.flip(frame, axis = 1)
    #converting image color from bgr to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #generating mask to protect red color
    lower_red = np.array([0,120,50])
    higher_red = np.array([0,255,255])
    mask_1 = cv2.inRange(hsv, lower_red, higher_red)
    
    lower_red = np.array([170,120,70])
    higher_red = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv, lower_red, higher_red)

    mask_1 = mask_1 + mask_2

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))
    
    #detecting path that doesn't have mask 1
    mask_2 = cv2.bitwise_not(mask_1)
    res_1 = cv2.bitwise_and(frame, frame, mask = mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)
    final_output = cv2.addWeighted(res_1, 1, res_2, 1,0)
    output_file.write(final_output)
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

cap.release()
output_file.release()
cv2.destroyAllWindows()