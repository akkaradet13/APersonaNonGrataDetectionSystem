import cv2

camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame
    ret, frame1 = camera1.read()
    ret, frame2 = camera2.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    print(frame1.shape, frame2.shape)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # cv2.imwrite(checkFileName(1),frame)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()