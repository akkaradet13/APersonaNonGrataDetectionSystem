import numpy as np
import cv2
import os

def checkFileName(n):
    entries = os.listdir('./dataSet4/')
    n = len(entries)+1
    name = f'img{str(n)}.png'
    return 'dataSet4/'+name

cap = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(f'{checkFileName(1)}',frame)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()