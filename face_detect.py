import argparse as arg
import time
import cv2
import numpy as np
from skin_seg import *
from FaceOrganDetect import *
from PushData import *
import os
import datetime

#! Face Detect
class Face_Detector():
    scale_factor = 3
    #! พื้นหลังขาว
    #     >   w , h
    size1 = (130,100)
    #     <   w , h
    size2 = (260,420)
    
    #! ทั่วไป
    #size1 = (50,50)
    #size2 = (400,400)
    
    def __init__(self,skin_detect,organ_detect,push_data):
        self._skin_detect = skin_detect
        self._organ_detect = organ_detect
        self._push_data = push_data
    @property
    def skin_detect(self):
        return self._skin_detect
    def Detect_Face_Img(self,img,size1,size2):
        skin_img = self._skin_detect.RGB_H_CbCr(img,False)
        contours, hierarchy = cv2.findContours(skin_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(img, contours, -1, (0,255,0), 1)
        # print(f'contours {contours}')
        # cv2.imshow("faces",img)
        # if cv2.waitKey(0) & 0xFF == ord("q"):
        # 	sys.exit(0)
        # print('contours',contours)
        # 
        print('shape',img.shape)
        rects = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # print(f'????{x} {y} {w} {h}')
            # multiplier = 1/self.scale_factor
            # if (w*multiplier > size1[0] and h*multiplier > size1[1]) and (w*multiplier < size2[0] and h*multiplier < size2[1]):
            if (w > size1[0] and h > size1[1]) and (w < size2[0] and h < size2[1]):
                Distance1 = 11.5*(img.shape[1]/float(w))
                Distance2 = 15.0*((img.shape[1] + 226.8)/float(w))
                print("\npinhole distance = {:.2f} cm\ncamera distance = {:.2f} cm".format(Distance1,Distance2))
                print("Width = {} \t Height = {}".format(w,h))
                if Distance1 < 50 and Distance2 < 90:
                    rects.append(np.asarray([x,y,w,w*1.25], dtype=np.uint16))
        return rects
    def Detect_Face_Vid(self,vid):	
        n = 0
        frameCounter = 0
        alpha = 0.2
        rects2 = None
        
        while True:
            start =time.time()
            (grabbed, img) = vid.read()
            img = cv2.flip(img, 1)
            if not grabbed:
                break
            fps = vid.get(cv2.CAP_PROP_FPS)
            
            # print("\nRecording at {} frame/sec".format(fps))
            # Image = cv2.resize(img, (0, 0), fx=1/self.scale_factor, fy=1/self.scale_factor)
            Image = img
            
            if frameCounter % 10 == 0:
                print('-------------------detec-----------------------')  
                rects = self.Detect_Face_Img(Image,self.size1,self.size2)
                face_crop = None
                organCheck = None
                textDraw = '...'
                print(f'len rects = {len(rects)} -> fps{fps}')
                if len(rects) == 0 :
                     rects2 = None
                else:
                    for i,r in enumerate(rects):
                        overlay = img.copy()            
                        x0,y0,w,h = r
                        face_crop = img[y0:y0+h, x0:x0+w]
                        # font = cv2.FONT_HERSHEY_SIMPLEX
                        LevelSecurity = open("./LevelSecurity.txt", "r").read()
                        print('LevelSecurity => ',LevelSecurity)
                        
                        organCheck = self._organ_detect.detect(face_crop)
                        print(organCheck)
                        if organCheck['Eyes'] is not None or organCheck['Nose'] is not None or organCheck['Mouth'] is not None:
                            rects2 = rects
                            cv2.rectangle(overlay, (x0,y0), (x0+w, y0+h), (0,0,255), 2)
                            
                            checkList = ''
                            #! Draw
                            for item in organCheck:
                                if organCheck[item] is not None:
                                    checkList += item[0]
                                    xod,yod,wod,hod = organCheck[item][0]
                                    print(f'rr{xod,yod,wod,hod}')
                                    xx = xod+x0
                                    yy = yod+y0
                                    if item == 'Eyes':
                                        for position in organCheck[item]:
                                            xod,yod,wod,hod = position
                                            print('eyePosition', xod,yod,wod,hod)
                                            cv2.rectangle(overlay, (xx, yy), (xx+wod, yy+hod), (0, 0, 255), 1)
                                            cv2.putText(overlay, str(item), (xx, yy-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 1, cv2.LINE_AA)
                                    else :
                                        cv2.rectangle(overlay, (xx, yy), (xx+wod, yy+hod), (0, 0, 255), 1)
                                        cv2.putText(overlay, str(item), (xx, yy-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 1, cv2.LINE_AA)
                                    
                                    # final_face = faceOrganDetect.detect(face_crop)
                                    # for item in final_face:
                                    #     if len(final_face[item]) > 0:
                                    #         x0,y0,w0,h0 = final_face[item]
                                    #         print(f'rr{x0,y0,w0,h0}')
                                    #         xx = x+x0
                                    #         yy = y+y0
                                    #         cv2.rectangle(img, (xx, yy), (xx+w0, yy+h0), (0, 0, 255), 1)
                           
                            fileName = ''
                            if len(checkList) >= int(LevelSecurity):
                                textDraw = 'Pass'
                                self.draw(overlay,'Pass')
                                cv2.imwrite(self.checkFileName(checkList,f'TestDetect/{str(LevelSecurity)}/Pass'), face_crop)
                                fileName = self.checkFileName(checkList,f'Data')
                                cv2.imwrite(fileName, face_crop)
                                f = open("./Actiondoor.txt", "w")
                                f.write("1")
                                f.close()
                            else:
                                textDraw = 'Not Pass'
                                self.draw(overlay,'Not Pass')
                                cv2.imwrite(self.checkFileName(checkList,f'TestDetect/{str(LevelSecurity)}/NotPass'), face_crop)
                                cv2.imwrite(self.checkFileName(checkList,f'Data'), face_crop)
                                f = open("./Actiondoor.txt", "w")
                                f.write("0")
                                f.close()
                            self._push_data.pushData(fileName)

                            print('checkList',checkList)
                            cv2.addWeighted(overlay, alpha, img, 1-alpha,0, img)
                            print(f'skin และ อวัยวะ {checkList} {len(checkList)}')
                        else:
                            print('skin แต่ ไม่เจออวัยวะ')
                            cv2.imwrite(self.checkFileName('none',f'TestDetect/{str(LevelSecurity)}/OnlySkin'), face_crop)
                            #cv2.imwrite(self.checkFileName('none',f'Data'), face_crop)
            else:
                print('-------------------else-------------------\n')
                #! Draw
                
                if rects2 is not None:
                    for i,r in enumerate(rects2):
                        overlay = img.copy()
                        
                        x0,y0,w,h = r
                        # x0 *= self.scale_factor
                        # y0 *= self.scale_factor
                        # w *= self.scale_factor
                        # h *= self.scale_factor
                        face_crop = img[y0:y0+h, x0:x0+w]
                        # font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.rectangle(overlay, (x0,y0), (x0+w, y0+h), (0,0,255),2)
                        print('final face',organCheck)
                        self.draw(overlay,textDraw)
                        
                        if organCheck is not None:
                            for item in organCheck:
                                if organCheck[item] is not None:
                                    xod,yod,wod,hod = organCheck[item][0]
                                    print(f'rr{xod,yod,wod,hod}')
                                    xx = xod+x0
                                    yy = yod+y0
                                    if item == 'Eyes':
                                        for position in organCheck[item]:
                                            xod,yod,wod,hod = position
                                            print('eyePosition', position)
                                            cv2.rectangle(overlay, (xx, yy), (xx+wod, yy+hod), (0, 0, 255), 1)
                                            cv2.putText(overlay, str(item), (xx, yy-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 1, cv2.LINE_AA)
                                    else :
                                        cv2.rectangle(overlay, (xx, yy), (xx+wod, yy+hod), (0, 0, 255), 1)
                                        cv2.putText(overlay, str(item), (xx, yy-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 1, cv2.LINE_AA)
                        cv2.addWeighted(overlay, alpha, img, 1-alpha,0, img)
                
                
            cv2.imshow('img', img)
            # print(f'frameCounter => {frameCounter}')
            if frameCounter > 30 : frameCounter = 0
            frameCounter += 1
            n += 1

            stop = time.time()
            frameRate = abs((1/fps - (stop - start)))
            # print(f'fram {frameRate}')
            time.sleep(frameRate)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        vid.release()
        
    def draw(self, overlay, text):
        cv2.putText(overlay, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 5, cv2.LINE_AA)


    def checkFileName(self, checkList, path):
        # entries = os.listdir('./face')
        #'2012-09-04 06:00:00.000000'
        x = datetime.datetime.now()
        x = str(x.strftime("%Y-%m-%d+%H:%M:%S_%f"))
        # return f'img{str(len(entries)+1)}.jpg'
        return f'{path}/{x}={checkList}=.jpg'

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
def open_camera(arg_):
    vid = cv2.VideoCapture(arg_)
    return vid
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please give me a file :Image/video !!!")
        print("\n Try Again, For more info type --help to see available options")
        sys.exit(0)
    in_arg = Arg_Parser()
    skin_detect = Skin_Detect()
    faceOrganDetect = FaceOrganDetect()
    pushData = PushData()
    
    Face_Detect = Face_Detector(skin_detect, faceOrganDetect, pushData)
    if in_arg["camera"] != None:
        cam = open_camera(int(in_arg["camera"]))
        Face_Detect.Detect_Face_Vid(cam)

