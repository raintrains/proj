import re
import json
import string



def open_json(path_file):
    
    with open(path_file, "r", encoding="UTF-8") as file:
        data = json.load(file)
    
    return data

def data_process_json(path_json):
    
    data_dict = {}
    
    data = open_json(path_file=path_json)
    
    pattern = r'^([^0-9]+)\s*(\d+(?:\.\d+)?)?\s*'

    pattern_for_check_digits = re.compile(r'\d')

    for d in data["receipts"][0]["items"]:
        
        name_dish = "".join([symbol for symbol in d["description"]]).rstrip()

        match = re.search(pattern, name_dish)


        if 'итого' in name_dish.lower():
            continue

        if (name_dish.split()[-1]).isdigit() and (name_dish.split()[-2]).isdigit():

            name_dish = " ".join(name_dish.split()[:-1])

        price_dish = int(d["amount"])
        
        if name_dish.lower() in ["сумма", "сума", "итого", "sum"]:
            break
        
        
        
        if d["unitPrice"] is not None:
            
            name_dish = match.group(1)

            data_dict.setdefault(re.sub(r'\d+', "", name_dish).rstrip().capitalize(), int(d["unitPrice"]))
        
        else:
            
            # print(name_dish)
            if name_dish.split()[-1].isdigit():
                # print("func 1", end="\n")
                # print(name_dish)

                amount = int(name_dish.split()[-1]) if 0 < int(name_dish.split()[-1]) < 10 else 1
                price_dish //= amount
                # print(f"Количество: {amount}")
                # print(price_dish)
                # print(name_dish)
            

                name_dish = re.sub(r'\d+', "", name_dish).rstrip()
                

            elif  name_dish.split()[-1][-1].isdigit():
                # print("func 2", end="\n")
                # print(name_dish)

                amount = int(name_dish.split()[-1][-1]) if 0 < int(name_dish.split()[-1][-1]) < 10 else 1
                # print(f"Количество: {amount}")
                price_dish //= amount

                # print(name_dish)

                name_dish = match.group(1).rstrip()
                if name_dish in data_dict.keys():
                    break
                # print(name_dish)

            else:
                pattern = r'^([^0-9]+)\s*(\d+(?:\.\d+)?)?\s*'
                match = re.search(pattern, name_dish)

                # print(name_dish)
                
                name_dish = match.group(1).rstrip()
                
                if match.group(2) is not None:
                    second_half = float(match.group(2))
                

                    if second_half:

                        if 1 < int(second_half) <= 10:
                            amount = int(second_half)
                            price_dish //= amount
                        else:
                            unit_price = int(second_half)
                            price_dish = unit_price
                    else:
                        price_dish = int(d['amount'])
                # print(name_dish)
            
            data_dict[name_dish.capitalize()] = data_dict.get(name_dish.capitalize(), 0) + price_dish            
    
        
        
    
    return data_dict

# print(data_process_json("receipt.json"))

# print(data_process_json("mac1.json"))
# for i in data_process_json("receipt.json").items():
#     print(*i, end="\n")
