import requests

import json



def asprise_process(image):

    url_asprise = "https://ocr.asprise.com/api/v1/receipt"

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

# asprise_process(r"photos/receipt.jpg")