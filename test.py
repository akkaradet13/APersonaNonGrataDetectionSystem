# import cv2
# import numpy as np

# img = cv2.imread("./img1.png")

# # First we crop the sub-rect from the image
# x, y, w, h = 100, 100, 200, 100
# # sub_img = img[y:y+h, x:x+w]
# sub_img = np.zeros((h,w,3), np.uint8)
# white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

# res = cv2.addWeighted(sub_img, 0, white_rect, 0, 0)

# # Putting the image back to its position
# img[y:y+h, x:x+w] = res
# cv2.imshow('img', img)
# x, y = 50, 50
# img[y:y+h, x:x+w] = res
# cv2.imshow('img2', img)


# cv2.waitKey(0)

import cv2

image = cv2.imread('img1.png')
overlay = image.copy()

x, y, w, h = 100, 100, 200, 100  # Rectangle parameters
cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 200, 0), -1)  # A filled rectangle

alpha = 0.4  # Transparency factor.

# Following line overlays transparent rectangle over the image
image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

cv2.imshow('s',image_new)
cv2.waitKey(0)