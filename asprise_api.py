import requests

import json

import pprint

import os

url_asprise = "https://ocr.asprise.com/api/v1/receipt"

files = os.listdir(r"photos")

if files:
    files = [os.path.join(r"photos", file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    path_last_image = max(files, key=os.path.getctime)


image = path_last_image

r = requests.post(url_asprise, data={ \
    
    "api_key": "TEST",
    "recognizer": "auto",
    "ref_no": "ocr_python_123",
    }, \
    files={"file": open(image, "rb")})

print(r.text)

formated_data = pprint.pformat(r.text, indent=4)

with open("receipt.json", "w", encoding="UTF-8") as file:
    file.write(formated_data + "\n")
# image.show()

