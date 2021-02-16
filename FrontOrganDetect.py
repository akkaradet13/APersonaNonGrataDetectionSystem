import cv2

class FrontOrganDetect():
    
    # Loading classifiers
    faceCascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    eyesCascade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')
    noseCascade = cv2.CascadeClassifier('xml/Nose.xml')
    mouthCascade = cv2.CascadeClassifier('xml/Mouth.xml')

    def __init__(self):
        pass
    
    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, text,frontOrganCheck):
        # Converting image to gray-scale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detecting features in gray-scale image, returns coordinates, width and height of features
        features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []
        # drawing rectangle around the feature and labeling it
        for (x, y, w, h) in features:
            # cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            # cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            coords = [x, y, w, h]
        frontOrganCheck[text] = coords
        # print(f'+++{text}==>{coords}')
        # if len(coords) <= 0 :
        #     frontOrganCheck[f'coords{text}'] = 0
        # else:
        #     print(f'{text} => {coords}')
        return frontOrganCheck

    # Method to detect the features
    def detect(self, img, option = 'all'):
        color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        frontOrganCheck = {'Eyes': None, 'Nose': None, 'Mouth': None}
        if option == 'eye':
            frontOrganCheck = self.draw_boundary(img, self.eyesCascade, 1.5, 4, color['red'], "Eyes", frontOrganCheck)
        else:
            frontOrganCheck = self.draw_boundary(img, self.eyesCascade, 1.5, 4, color['red'], "Eyes", frontOrganCheck)
            frontOrganCheck = self.draw_boundary(img, self.noseCascade, 1.5, 4, color['green'], "Nose", frontOrganCheck)
            frontOrganCheck = self.draw_boundary(img, self.mouthCascade, 1.5, 2, color['white'], "Mouth", frontOrganCheck)
            # print(f'+++++{frontOrganCheck}')
        return frontOrganCheck
    
'''

'''