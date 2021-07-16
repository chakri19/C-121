import cv2
import time
import numpy as np
import keyboard

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
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)
    #converting image color from bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    frame = cv2.resize(frame, (640,480))
    image = cv2.resize(image, (640,480))

    #generating mask to protect black color
    l_black = np.array([30,30,0])
    u_black = np.array([104,153,70])

    mask = cv2.inRange(frame, l_black, u_black)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    f = frame * res
    f = np.where(f == 0, image, f)

    if keyboard.is_pressed("Esc"):
        break
    if keyboard.is_pressed("Q"):
        break

cap.release()
output_file.release()
cv2.destroyAllWindows()