import cv2

cap = cv2.VideoCapture('output.avi')
face_detector = cv2.CascadeClassifier('./xml/haarcascade_frontalface_default.xml')
tracker = cv2.TrackerMIL_create()
onTracking = False
count = 0

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.1, 4)
    if not onTracking:
        print(f'faces{faces}')
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            onTracking = tracker.init(frame, (x,y,w,h))
            onTracking = True
            print(f'{x} {y} {w} {h}')
            cv2.imshow('img', frame)
    else:
        ok, bbox = tracker.update(frame)
        xt,yt,wt,ht = bbox
        cv2.rectangle(frame, (xt, yt), (xt+wt, yt+ht), (0, 0, 255), 2)
        cv2.imshow('img1', frame)
    if count == 30:
        onTracking = False
        count = 0
    print(f'count{count}')
    count += 1
    # Display
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()