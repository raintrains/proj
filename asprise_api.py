import requests

import json

import os



def asprise_process(image):

    url_asprise = "https://ocr.asprise.com/api/v1/receipt"

    # files = os.listdir(r"photos")

    # if files:
    #     files = [os.path.join(r"photos", file) for file in files]
    #     files = [file for file in files if os.path.isfile(file)]
    #     path_last_image = max(files, key=os.path.getctime)


    data = {

        "api_key": "TEST",
        "recognizer": "auto",
        "ref_no": "ocr_python_123",

        }


    r = requests.post(url_asprise, data, files={"file":open(image, "rb")})

    try:
        
        with open("receipt.json", "w", encoding="UTF-8") as file:
            json.dump(r.json(), file, indent=4, ensure_ascii=False)

        return("Обработано!")
    
    except:

        return("Error!")
