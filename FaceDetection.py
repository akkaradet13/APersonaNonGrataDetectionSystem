import cv2
import os
from datetime import date
from datetime import datetime

today = date.today()
dateNow = today.strftime('%d%m%y')

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def faceDetec(faces):
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/" + str(dateNow) + '#' +  str(datetime.now()) + '.' + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
# For each person, enter one numeric face id
while(True):
    ret, img = cam.read()
    # img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    print(type(faces))
    if type(faces) != 'tuple':
        faceDetec(faces)
        
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()