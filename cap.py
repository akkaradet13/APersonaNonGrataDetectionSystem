import numpy as np
import cv2
import os

def checkFileName(n):
    name = f'img{n}.jpg'
    entries = os.listdir('asset/')
    print(entries, name)
    if name in entries:
        n += 1
        checkFileName(n)
        print('0')
    else :
        # name = f'asset/{name}'
        print(name)
        return name
    
    # for i in entries:
    #     name = f'asset/img{n}.jpg'
    #     if name in entries:
    #         n += 1
    #         print('ok')
    #     else:
    #         print(name)
    #         return name

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(checkFileName(1),frame)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()