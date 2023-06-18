import os

from PIL import Image, ImageEnhance, ImageFilter

import cv2
import pytesseract

import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

trained_data_path = r'C:\\Program Files\\Tesseract-OCR\\tessdata'

custom_config = r"--oem 3 --psm 3"
files = os.listdir(r"photos")

if files:
    files = [os.path.join(r"photos", file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    path_last_image = max(files, key=os.path.getctime)

#   Pillow

    # image = Image.open(path_last_image)

    # enhancer = ImageEnhance.Contrast(image)
    # enhanced_image = enhancer.enhance(4)

    # sharpened_image = enhanced_image.filter(ImageFilter.SHARPEN)

    # binary_image = sharpened_image.convert("L")
    # treshold = 128
    # binary_image = binary_image.point(lambda x: 0 if x < treshold else 255, "1")

    # binary_image = binary_image.convert("RGB")

    # brightness = 1
    # contrast = 4
    # adjusted_image = ImageEnhance.Brightness(binary_image).enhance(brightness)
    # adjusted_image = ImageEnhance.Contrast(adjusted_image).enhance(contrast)

    # adjusted_image.show()

#   CV2
    img = cv2.imread(path_last_image)
    # img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)

    # cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
#   Pytesseract
    cv2.imshow("i", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    text = pytesseract.image_to_string(img, config=custom_config, lang="ukr")

    print(text)

#   Other

    # cleaned_text = text.replace("/n", " ")

with open("row_text.txt", "w", encoding="UTF-8") as file:
    file.write(text)
    