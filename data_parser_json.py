import re
import json
import string



def open_json():
    
    with open("receipt.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    
    return data

def data_process_json():
    
    data_dict = {}
    
    punc = string.punctuation
    
    for d in open_json()["receipts"][0]["items"]:
        
        name_dish = "".join([symbol for symbol in d["description"] if symbol not in punc]).rstrip()
    
        if (name_dish.split()[-1]).isdigit() and (name_dish.split()[-2]).isdigit():
            
            name_dish = " ".join(name_dish.split()[:-1])
    
        price_dish = int(d["amount"])
        
        if name_dish.lower() in ["сумма", "сума", "итого", "sum"]:
            break
        
        try:
        
            if d["unitPrice"] is not None:
                
                data_dict.setdefault(re.sub(r'\d+', "", name_dish).rstrip().capitalize(), int(d["unitPrice"]))
            
            else:
                if name_dish.split()[-1].isdigit():
                    
                    price_dish //= int(name_dish.split()[-1])
                    name_dish = re.sub(r'\d+', "", name_dish).rstrip()
                data_dict[name_dish.capitalize()] = data_dict.get(name_dish, 0) + price_dish
            
    
        
        except:
            pass
    

    return data_dict