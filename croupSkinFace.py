import cv2
import numpy as np
from skin_seg import *
from imutils import paths
import argparse , collections
import os
import pandas as pd

name = []
list_x = []
list_y = []
list_w = []
list_h = []
predict = []
def Detect_Face_Img(_skin_detect,img):
    skin_img = _skin_detect.RGB_H_CbCr(img,False)
    print('skin_img',type(skin_img))
    print(np.count_nonzero(skin_img==1))
    print(np.count_nonzero(skin_img==0))
    np.savetxt("foo.csv", skin_img, delimiter=",")
    contours, hierarchy = cv2.findContours(skin_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0), 1)
    # print(f'contours {hierarchy}')
    n = 0
    for c in contours:
        # bounding = cv2.boundingRect(c)
        x,y,w,h = cv2.boundingRect(c)
        if w > 142 :
            # Distance1 = 11.5*(img.shape[1]/float(w))
            # Distance2 = 15.0*((img.shape[1] + 226.8)/float(w))
            # print("\npinhole distance = {:.2f} cm\ncamera distance = {:.2f} cm".format(Distance1,Distance2))
            # print("Width = {} \t Height = {}".format(w,h))
            
            # print(f'contour => {c}')
            # rect = cv2.minAreaRect(c)
            # box = cv2.boxPoints(rect)
            # box = np.int0(box)
            # cv2.drawContours(img,[box],0,(0,0,255),2)
            
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            skin = img[y:y+h, x:x+w]
            cv2.imshow(str(n),skin)
            print(f' +++ {x, y, w, h} {w*h}')
            name.append(f'{img}_{n}')
            list_x.append(x)
            list_y.append(y)
            list_w.append(w)
            list_h.append(h)
            # p = str(input('predict: '))
            # p = n
            # predict.append(p)
            n += 1
    # cv2.imshow("faces",img)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        # df = pd.DataFrame({'name': name, 'x':list_x, 'y':list_y, 'h':list_h, 'w':list_w, 'predict':predict})
        # df.to_excel('./states.xlsx', sheet_name='States', index=False)
        sys.exit(0)
        
#! -----------------------------------------------
skin_detect = Skin_Detect()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
args = vars(ap.parse_args())
imagePath = args["images"]
image = cv2.imread(imagePath)
Detect_Face_Img(skin_detect,image)

entries = os.listdir('dataSet2/')
print(len(entries))
