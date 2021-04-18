import numpy as np
import cv2
import time
from win10toast import ToastNotifier

capture = cv2.VideoCapture(0)  # Can replace 0 with 'path to a .mp4 video', will use video instead of a live webcam
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
notif = ToastNotifier()
DELAY = 3600    # Default 1 hour delay
notifTime = -1 * DELAY
counterTime = time.time()
falseCounter = 0
#delays = [1200, 1800, 3600, 7200]
#global currentDelay
#currentDelay = 2

width = int(capture.get(3))
height = int(capture.get(4))


#def onMouse(event, x, y, flags, currentDelay, param):
#    if event == cv2.EVENT_LBUTTONDOWN:
#        if 0 < x < 100 and height - 50 < y < height:
#            currentDelay = currentDelay + 1
#            DELAY = delays[currentDelay]

while True:
    ret, frame = capture.read()    # ret will be False if error trying to get frame
#    cv2.rectangle(frame, (0, height - 50), (100, height), (34, 139, 34), -1)
#    cv2.rectangle(frame, (0, height - 50), (100, height), (0, 255, 255), 5)

#    font = cv2.FONT_HERSHEY_COMPLEX
#    frame = cv2.putText(frame, str(DELAY), (5, height - 10), font, 1.1, (0, 0, 0), 2, cv2.LINE_AA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3 , 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

    currentTime = time.time()
    if len(faces) == 0 and currentTime >= notifTime + DELAY:

        if falseCounter <= 10 and currentTime > counterTime + 10:
            notifTime = time.time()
            counterTime = time.time()
            notif.show_toast('Preposterous Posture', 'You have bad posture!\nTry sitting up a little more straight.', duration = 3, threaded = True)
            falseCounter = 0        
        elif currentTime > counterTime + 10:
            falseCounter = 0
            counterTime = time.time()
    elif currentTime < counterTime + 10 and len(faces) != 0:
        falseCounter = falseCounter + 1
    elif currentTime >= counterTime + 10:
        falseCounter = 0
        counterTime = time.time()
    print(falseCounter)

    cv2.imshow('Video Feed', frame)   # Displays video

#    cv2.setMouseCallback('Video Feed', onMouse)



    if cv2.waitKey(1) == 27:
        break                   # Breaks out of the while loop then if q is pressed
    
capture.release()                  # Releases the camera resource
cv2.destroyAllWindows()