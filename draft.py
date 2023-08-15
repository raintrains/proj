import json

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, parent_dir)

from data_parser_json import data_process_json


EXPECTED_RESULT = {
    "test_sazha_data": {

        'Jagermeister': 85,
        'Грімберген дабл амбрi': 90, 
        'Узвар': 23, 
        'Кьянти': 120, 
        'Гриби печерицi гриль': 40, 
        'Овочi гриль цукини': 40, 
        'Шашлик з кур. стегна в': 175, 
        'Картопля печена на манг': 20, 
        'Вареники з кроликом': 145, 
        'Деруни з грибами': 92, 
        'Цезар класичний з філе': 162, 
        'Гнiздечко з вершк.coyco': 115, 
        'Грiмберген блонд': 90, 
        'Риба дорадо': 125

    },

    "test_mac1": {

        'Хеппі міл чізбургер': 50, 
        'Іграшка хм': 32, 
        'Максанді полуничне': 35, 
        'Полива полунична': 8, 
        'Біг мак': 62, 
        'Сер картопля фрi': 31, 
        'Еспресо': 19, 
        'Макпиріг вишневий': 25, 
        'Пиріг каранель-поколад': 29

    }
}




prepared_data = data_process_json("receipt.json")

print(prepared_data)

valid_key = ""

for key, value in EXPECTED_RESULT.items():
   if set(list(value.keys())).issubset(prepared_data):
      print("ok")
      valid_key = key




