''' usage :
1- python3 face_detect.py -v videos/test1.mkv
2- python3 face_detect.py -i images/img3.jpg
'''
import argparse as arg
import time
import cv2
import numpy as np
from skin_seg import *
import os

#! Face Detect
class Face_Detector():
    # faceCascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    # eyesCascade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')
    # noseCascade = cv2.CascadeClassifier('xml/Nose.xml')
    # mouthCascade = cv2.CascadeClassifier('xml/Mouth.xml')
    def __init__(self,skin_detect):
        "skin_detect is an object from skin_seg file"
        self._skin_detect = skin_detect
    @property
    def skin_detect(self):
        "set skin_detect to be an immutable field/property"
        return self._skin_detect
    def Detect_Face_Img(self,img,size1,size2):
        '''this method implements the skin detection algorithm to perform a face detection in a given image.
        -inputs: 
        img : BGR image (numpy array)
        size1 : the lower size of a rectangle/face(min size) (type tuple)
        size2 : the upper size of a rectangle/face(max size) (type tuple)
        -output:
        a numpy array with all faces coordinates in a picture.
        '''
        #get the RGB_H_CbCr representation of the image(for more info, please refer to skin_seg.py)
        skin_img = self._skin_detect.RGB_H_CbCr(img,False)
        contours, hierarchy = cv2.findContours(skin_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2	.drawContours(img, contours, -1, (0,255,0), 1)
        #cv2.imshow("faces",img)
        #if cv2.waitKey(0) & 0xFF == ord("q"):
        #	sys.exit(0)
        rects = []
        for c in contours:
            # get the bounding rect
            x, y, w, h = cv2.boundingRect(c)
            # draw a green rectangle to visualize the bounding rect
            if (w > size1[0] and h > size1[1]) and (w < size2[0] and h < size2[1]):
                #pinhole distance
                Distance1 = 11.5*(img.shape[1]/float(w))
                #camera distance
                Distance2 = 15.0*((img.shape[1] + 226.8)/float(w))
                print("\npinhole distance = {:.2f} cm\ncamera distance = {:.2f} cm".format(Distance1,Distance2))
                print("Width = {} \t Height = {}".format(w,h))
                rects.append(np.asarray([x,y,w,w*1.25], dtype=np.uint16))
        return rects
    def Detect_Face_Vid(self,vid,size1,size2,scale_factor = 3):
        '''this method implements the skin detection algorithm to perform a face detection in a given video file.
        -inputs: 
        vid : video object 
        size1 : the lower size of a rectangle/face(min size) (type tuple)
        size2 : the upper size of a rectangle/face(max size) (type tuple)
        scale_factor : parameter for scaling down the image for a better frame rate
        -output:
        void
        '''		
        n = 0
        while True:
            start =time.time()
            (grabbed, img) = vid.read()
            if not grabbed:
                break
            #get the frame rate
            fps = vid.get(cv2.CAP_PROP_FPS)
            print("\nRecording at {} frame/sec".format(fps))
            Image = cv2.resize(img, (0, 0), fx=1/scale_factor, fy=1/scale_factor)
            rects = self.Detect_Face_Img(Image,size1,size2)
            face_crop = None
            final_face = None
            for i,r in enumerate(rects):
                # Scale back up face locations since the frame we detected in was scaled to 1/10 size
                x0,y0,w,h = r
                x0 *= scale_factor
                y0 *= scale_factor
                w *= scale_factor
                h *= scale_factor
                # cv2.rectangle(img, (x0,y0),(x0+w,y0+h),(0,255,0),1)
                face_crop = img[y0:y0+h, x0:x0+w]
                font = cv2.FONT_HERSHEY_SIMPLEX
            stop = time.time()
            # f = 30 frame/sec
            # T = 1/30 sec/frame
            # T = 0.032
            #frame = cv2.resize(frame, dim, interpolation =  cv2.INTER_AREA)
            time.sleep(abs((1/fps - (stop - start))))
            # cv2.imshow('faces', face_crop)
            final_face = detect(face_crop, eyesCascade, noseCascade, mouthCascade)
            cv2.imshow(str(n),final_face)
            # n += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        vid.release()

#! FrontOrganDetect
# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text,frontOrganCheck):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
        #? ------------------------- ยังทำไม่ได้
    if len(coords) <= 0 :
        print(f'No!!! => {text}')
    else:
        frontOrganCheck[text] = 1
        print(f'{text} => {coords}')
    return frontOrganCheck

# Method to detect the features
def detect(img, eyeCascade, noseCascade, mouthCascade):
    frontOrganCheck = {'Eyes':0, 'Nose':0, 'Mouth':0}
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    frontOrganCheck = draw_boundary(img, eyeCascade, 1.1, 12, color['red'], "Eyes", frontOrganCheck)
    frontOrganCheck = draw_boundary(img, noseCascade, 1.1, 4, color['green'], "Nose", frontOrganCheck)
    frontOrganCheck = draw_boundary(img, mouthCascade, 1.1, 20, color['white'], "Mouth", frontOrganCheck)
    print(f'+++++{frontOrganCheck} \n -----{checkOrgan(frontOrganCheck)}')
    return img

def checkOrgan(frontOrganCheck):
    data = ''
    for Organ in frontOrganCheck:
        if frontOrganCheck[Organ] == 1:
            data += Organ[0]
    
    return data 


# Loading classifiers
faceCascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')
noseCascade = cv2.CascadeClassifier('xml/Nose.xml')
mouthCascade = cv2.CascadeClassifier('xml/Mouth.xml')

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
    size1 = (40,40)
    size2 = (300,400)
    scale_factor = 3
    Face_Detect = Face_Detector(skin_detect)
    if in_arg["image"] != None:
        img = open_img(in_arg)
        rects = Face_Detect.Detect_Face_Img(img,size1,size2)
        print('rects',rects)
        n = 1
        final_face = None
        for i,r in enumerate(rects):
            x,y,w,h = r
            #face = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
            face_crop = img[y:y+h, x:x+w]
            final_face = detect(face_crop, eyesCascade, noseCascade, mouthCascade)
            cv2.imshow(str(n),final_face)
            n += 1
            print('---------------')
            try:
                cv2.imwrite('face/'+checkFileName(), final_face)
                print(f'{n}detect')
            except:
                print('0')
        #cv2.imshow("faces",img)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            sys.exit(0)
    if in_arg["video"] != None:
        vid = open_vid(in_arg)
        Face_Detect.Detect_Face_Vid(vid,size1,size2,scale_factor)
    if in_arg["camera"] != None:
        cam = open_camera()
        Face_Detect.Detect_Face_Vid(cam,size1,size2,scale_factor)

