import cv2
import numpy as np
from skin_seg import *
eye_cascade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')

def Detect_Face_Img(_skin_detect,img):
    skin_img = _skin_detect.RGB_H_CbCr(img,False)
    contours, hierarchy = cv2.findContours(skin_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0), 1)
    # print(f'contours {contours}')
    n = 0
    for c in contours:
        bounding = cv2.boundingRect(c)
        x,y,w,h = cv2.boundingRect(c)
        # print(f'contour => {c} /n bounding  x y w h=> {bounding} ')
        if w > 100 :
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            print(f'{n} => x{x} y{y} w{w} h{h}')
            # x,y,w,h = x+20, y+13, w-40, h-80
            skin = img[y:y+h, x:x+w]
            print(skin.shape)
            cv2.imshow(str(n),skin)
            eyes = eye_cascade.detectMultiScale(skin)
            # print(f'eyes => {eyes}')
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(skin,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            n += 1
    cv2.imshow("faces",img)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        sys.exit(0)
skin_detect = Skin_Detect()
# img = cv2.imread('./face/img3.jpg')
# Detect_Face_Img(skin_detect,img)

# import the necessary packages
from imutils import paths
import argparse
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
args = vars(ap.parse_args())
# loop over the input images
imagePath = args["images"]
	# load the image, convert it to grayscale, and compute the
	# focus measure of the image using the Variance of Laplacian
	# method
image = cv2.imread(imagePath)
Detect_Face_Img(skin_detect,image)

	# cv2.imshow("Image", image)
	# key = cv2.waitKey(0)