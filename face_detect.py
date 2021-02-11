import argparse as arg
import time
import cv2
import numpy as np
from skin_seg import *
from FrontOrganDetect import *
import os

#! Face Detect
class Face_Detector():
    def __init__(self,skin_detect,organ_detect):
        self._skin_detect = skin_detect
        self._organ_detect = organ_detect
    @property
    def skin_detect(self):
        return self._skin_detect
    def Detect_Face_Img(self,img,size1,size2):
        skin_img = self._skin_detect.RGB_H_CbCr(img,False)
        contours, hierarchy = cv2.findContours(skin_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # cv2	.drawContours(img, contours, -1, (0,255,0), 1)
        # print(f'contours {contours}')
        # cv2.imshow("faces",img)
        # if cv2.waitKey(0) & 0xFF == ord("q"):
        # 	sys.exit(0)
        rects = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (w > size1[0] and h > size1[1]) and (w < size2[0] and h < size2[1]):
                Distance1 = 11.5*(img.shape[1]/float(w))
                Distance2 = 15.0*((img.shape[1] + 226.8)/float(w))
                print("\npinhole distance = {:.2f} cm\ncamera distance = {:.2f} cm".format(Distance1,Distance2))
                print("Width = {} \t Height = {}".format(w,h))
                rects.append(np.asarray([x,y,w,w*1.25], dtype=np.uint16))
        return rects
    def Detect_Face_Vid(self,vid,size1,size2,scale_factor = 3):	
        n = 0
        frameCounter = 0
        while True:
            start =time.time()
            (grabbed, img) = vid.read()
            if not grabbed:
                break
            fps = vid.get(cv2.CAP_PROP_FPS)
            print("\nRecording at {} frame/sec".format(fps))
            Image = cv2.resize(img, (0, 0), fx=1/scale_factor, fy=1/scale_factor)
            if frameCounter % 3 > 0:
                print('-------------------detec-----------------------')  
                rects = self.Detect_Face_Img(Image,size1,size2)
                face_crop = None
                final_face = None
                print(f'len rects = {len(rects)} -> fps{fps}')
                for i,r in enumerate(rects):
                    x0,y0,w,h = r
                    x0 *= scale_factor
                    y0 *= scale_factor
                    w *= scale_factor
                    h *= scale_factor
                    face_crop = img[y0:y0+h, x0:x0+w]
                    # font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(img, (x0,y0), (x0+w, y0+h), (0,255,0))
                    final_face = self._organ_detect.detect(face_crop)
                    for item in final_face:
                        if len(final_face[item]) > 0:
                            xod,yod,wod,hod = final_face[item]
                            print(f'rr{xod,yod,wod,hod}')
                            xx = xod+x0
                            yy = yod+y0
                            cv2.rectangle(img, (xx, yy), (xx+wod, yy+hod), (0, 0, 255), 1)
                            cv2.putText(img, str(item), (xx, yy-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 1, cv2.LINE_AA)
            cv2.imshow('img', img)
            stop = time.time()
            frameRate = abs((1/fps - (stop - start)))
            print(f'fram {frameRate}')
            time.sleep(frameRate)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            print(f'frameCounter => {frameCounter}')
            frameCounter += 1
            if frameCounter > 30 : frameCounter = 0
        vid.release()

def checkFileName():
    entries = os.listdir('./face')
    return f'img{str(len(entries)+1)}.jpg'

#! Main
def Arg_Parser():
    Arg_Par = arg.ArgumentParser()
    Arg_Par.add_argument("-i", "--image", help = "relative/absolute path of the image file")
    Arg_Par.add_argument("-v", "--video", help = "relative/absolute path of the recorded video file")
    Arg_Par.add_argument("-c", "--camera",help = "camera")
    arg_list = vars(Arg_Par.parse_args())
    return arg_list
def open_img(arg_):
    mg_src = arg_["image"]
    img = cv2.imread(mg_src)
    img_arr = np.array(img, 'uint8')
    return img_arr	 
def open_vid(arg_):
    vid_src = "videos/video1.mkv"
    vid = cv2.VideoCapture(arg_["video"])
    return vid
def open_camera():
    vid = cv2.VideoCapture(0)
    return vid
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please give me a file :Image/video !!!")
        print("\n Try Again, For more info type --help to see available options")
        sys.exit(0)
    in_arg = Arg_Parser()
    skin_detect = Skin_Detect()
    frontOrganDetect = FrontOrganDetect()
    size1 = (20,20)
    size2 = (150,150)
    # size1 = (50,50)
    # size2 = (400,400)
    scale_factor = 3
    Face_Detect = Face_Detector(skin_detect, frontOrganDetect)
    if in_arg["image"] != None:
        img = open_img(in_arg)
        rects = Face_Detect.Detect_Face_Img(img,size1,size2)
        print('rects',rects)
        n = 1
        face_crop = None
        for i,r in enumerate(rects):
            x,y,w,h = r
            face = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
            face_crop = img[y:y+h, x:x+w]
            final_face = frontOrganDetect.detect(face_crop)
            for item in final_face:
                if len(final_face[item]) > 0:
                    x0,y0,w0,h0 = final_face[item]
                    print(f'rr{x0,y0,w0,h0}')
                    xx = x+x0
                    yy = y+y0
                    cv2.rectangle(img, (xx, yy), (xx+w0, yy+h0), (0, 0, 255), 1)
            print(f'frontOrganDetect {n} ==> {final_face} \n')
            n += 1
            # try:
            #     cv2.imwrite('face/'+checkFileName(), final_face)
            #     print(f'{n}detect')
            # except:
            #     print('0')
        cv2.imshow('img',img)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            sys.exit(0)
    if in_arg["video"] != None:
        vid = open_vid(in_arg)
        Face_Detect.Detect_Face_Vid(vid,size1,size2,scale_factor)
    if in_arg["camera"] != None:
        cam = open_camera()
        Face_Detect.Detect_Face_Vid(cam,size1,size2,scale_factor)

