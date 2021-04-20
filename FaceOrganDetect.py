import cv2

class FaceOrganDetect():
    
    # Loading classifiers
    eyesCascade = cv2.CascadeClassifier('xml/haarcascade_eye_tree_eyeglasses.xml')
    noseCascade = cv2.CascadeClassifier('xml/haarcascade_mcs_nose.xml')
    mouthCascade = cv2.CascadeClassifier('xml/haarcascade_mcs_mouth.xml')
    
    def detectOrgan(self, img, classifier, scaleFactor, minNeighbors, color, text,faceOrganCheck, minSize=(5,5), maxSize=(100,100)):
        ds_factor = 0.5
        # img = cv2.resize(img, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray_img = cv2.bilateralFilter(gray_img,5,1,1) 
        # detecting features in gray-scale image, returns coordinates, width and height of features
        if text == 'Eyes':
            # features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors,minSize=(10,30))
            features = classifier.detectMultiScale(gray_img)
        else:
            features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors, minSize=minSize, maxSize=maxSize)
        if len(features) <= 0 :
            features = None
        print(f'{text} => {features}')
        faceOrganCheck[text] = features
        return faceOrganCheck

    # Method to detect the features
    def detect(self, img, option = 'all'):
        color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        faceOrganCheck = {'Eyes': None, 'Nose': None, 'Mouth': None}
        faceOrganCheck = self.detectOrgan(img, self.eyesCascade, 1.05, 5, color['red'], "Eyes", faceOrganCheck,minSize=(50,30), maxSize=(80,50))
        faceOrganCheck = self.detectOrgan(img, self.noseCascade, 1.05, 5, color['green'], "Nose", faceOrganCheck,minSize=(100,100), maxSize=(150,150))
        faceOrganCheck = self.detectOrgan(img, self.mouthCascade, 1.05, 5, color['white'], "Mouth", faceOrganCheck,minSize=(120,60), maxSize=(170,110))
            # print(f'+++++{faceOrganCheck}')
        return faceOrganCheck