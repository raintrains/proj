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
        
        try:
        
            if d["unitPrice"] is not None:
                
                name_dish = match.group(1)

                data_dict.setdefault(re.sub(r'\d+', "", name_dish).rstrip().capitalize(), int(d["unitPrice"]))
            
            else:
                
                if name_dish.split()[-1].isdigit():
                    # print("func 1", end="\n")
                    # print(name_dish)

                    amount = int(name_dish.split()[-1]) if 0 < int(name_dish.split()[-1]) < 10 else 1
                    # print(f"Количество: {amount}")
                    price_dish //= amount

                    name_dish = re.sub(r'\d+', "", name_dish).rstrip()
                    

                elif  name_dish.split()[-1][-1].isdigit():
                    # print("func 2", end="\n")
                    # print(name_dish)

                    amount = int(name_dish.split()[-1][-1]) if 0 < int(name_dish.split()[-1][-1]) < 10 else 1
                    # print(f"Количество: {amount}")
                    price_dish //= amount

                    # print(name_dish)

                    name_dish = match.group(1).rstrip()

                    if name_dish in data_dict:
                        break

                else:
                
                    pattern = r'^([^0-9]+)\s*(\d+(?:\.\d+)?)?\s*'
                    match = re.search(pattern, name_dish)


                    name_dish = match.group(1).rstrip()

                    if match.group(2):
                        price_dish //= int(match.group(2))

                data_dict[name_dish.capitalize()] = data_dict.get(name_dish.capitalize(), 0) + price_dish
            
    
        
        except:
            pass
    
    return data_dict

# print(data_process_json("receipt.json"))
for i in data_process_json("receipt.json").items():
    print(*i, end="\n")

'''
# отсутствует Кава Американо
# Картопля"по-домашньому" 250  ---> Картопля"по-домашньому" 125
# Пампушка з часничком 150  ---> Пампушка з часничком 15
# Ребра bbq 1  ---> Ребра bbq 520
# Ворель у прованських травах 191  ---> Ворель у прованських травах 250
# Рулька свинна з тушкованою 400  ---> Рулька свинна з тушкованою 160 
'''