"""https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/"""



import cv2
import pytesseract
import numpy as np



from transform import four_point_transform

from skimage.filters import threshold_local

import numpy as np
import cv2
import imutils
import os


files = os.listdir(r"photos")

if files:
    files = [os.path.join(r"photos", file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    path_last_image = max(files, key=os.path.getctime)



image = cv2.imread(path_last_image)
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(image, 50, 150)

# print("STEP 1: Edge Detection")
# cv2.imshow("Image", image)
# cv2.moveWindow("Image", 0, 0)
# cv2.imshow("Edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]


for c in cnts:
    
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break

# print("STEP 2: Find countours of paper")
# cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
# cv2.imshow("Outline", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method="gaussian")
warped = (warped > T).astype("uint8") * 255

cv2.imwrite(r"photos\scanned.jpg", imutils.resize(warped, height=650))

cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped, height=650))
cv2.moveWindow("Scanned", 0, 0)

cv2.waitKey(0)
