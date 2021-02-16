import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('./xml/haarcascade_frontalface_default.xml')
eye_detector = cv2.CascadeClassifier('./xml/haarcascade_eye.xml')
mouth_detector = cv2.CascadeClassifier('./xml/haarcascade_mcs_mouth.xml')
Nose_detector = cv2.CascadeClassifier('./xml/haarcascade_mcs_nose.xml')
alpha = 0.2
n = 0
faces = None
while True :
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = frame
    if n%10 == 0:
        faces = face_detector.detectMultiScale(gray, 1.1, 4)
        print(f'face => {len(faces)}')
        if len(faces) <= 0 :
                output = frame
        else:
            for (x, y, w, h) in faces:
                    overlay = frame.copy()
                    output = frame.copy()
                    cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 0, 255), -1)
                    cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
                    # roi_gray = gray[y:y+h, x:x+w]
                    # roi_color = frame[y:y+h, x:x+w]
                    
                    # eyes = eye_detector.detectMultiScale(roi_gray)
                    # print(f'eye {eyes}')
                    # for (ex,ey,ew,eh) in eyes:
                    #         cv2.putText(frame, 'eye', (ex,ey), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
                    #         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                            
                    # mouth = mouth_detector.detectMultiScale(roi_gray, 1.3, 5)
                    # print(f'mouth {mouth}')
                    # for (mx, my, mw, mh) in mouth:
                    #         cv2.putText(frame, 'mouth', (mx,my), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
                    #         cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,255,0),2)
                            
                    # nose = Nose_detector.detectMultiScale(roi_gray, 1.3, 5)
                    # print(f'nose {nose}')
                    # for (nx, ny, nw, nh) in nose:
                    #         cv2.putText(frame, 'nose', (nx,ny), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
                    #         cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,255,0),2)
    else:
        print('else')
        for (x, y, w, h) in faces:
                    overlay = frame.copy()
                    output = frame.copy()
                    cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 0, 255), -1)
                    cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
        
    n += 1
    if n == 30 : n = 0
    cv2.imshow('img', output)
    
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()