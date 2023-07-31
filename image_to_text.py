import os

from PIL import Image, ImageEnhance, ImageFilter

import cv2
import pytesseract

import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# trained_data_path = r'/usr/share/tesseract-ocr/4.00/tessdata'


custom_config = r"--oem 1 --psm 12"
files = os.listdir(r"photos")

if files:
    files = [os.path.join(r"photos", file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    path_last_image = max(files, key=os.path.getctime)

    img = cv2.imread(path_last_image)
   
    # cv2.imshow("i", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    text = pytesseract.image_to_string(img, config=custom_config, lang="ukr")

    print(text)

    # image  = Image.open(path_last_image)
# 
    # data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang="ukr")

    # print(data)
    # text_with_formating = ''

    # for i, word_text in enumerate(data["text"]):
    #     if word_text.strip():
    #         left = data["left"][i]
    #         top = data["top"][i]
    #         width = data["width"][i]
    #         height = data["height"][i]
    #         text_with_formating += f"{word_text}"
    #         if left + width < image.width:
    #             next_word_left = data["left"][i + 1]
    #             if next_word_left > left + width:
    #                 text_with_formating += "\n"
    # print(text_with_formating)

# with open("row_text.txt", "w", encoding="UTF-8") as file:
    # file.write(text)
    