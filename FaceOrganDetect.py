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
        '''
        if text == 'Eyes':
            # features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors,minSize=(10,30))
            features = classifier.detectMultiScale(gray_img)
        elif text != 'Eyes':
            # features = classifier.detectMultiScale(gray_img)
            '''
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
        faceOrganCheck = self.detectOrgan(img, self.eyesCascade, 1.1, 3, color['red'], "Eyes", faceOrganCheck,minSize=(40,45), maxSize=(55,55))
        faceOrganCheck = self.detectOrgan(img, self.noseCascade, 1.3, 2, color['green'], "Nose", faceOrganCheck,minSize=(55,65), maxSize=(65,75))
        faceOrganCheck = self.detectOrgan(img, self.mouthCascade, 1.2, 3, color['white'], "Mouth", faceOrganCheck,minSize=(40,75), maxSize=(50,85))
            # print(f'+++++{faceOrganCheck}')
        return faceOrganCheck
    
# type w   h   c
# eye (20, 50, 3)
# eye (23, 50, 3)
# nose (60, 71, 3)
# mouth (45, 83, 3)