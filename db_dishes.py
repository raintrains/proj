import sqlite3
import json





def create_db_dishes():

    with open("receipt1.json", "r", encoding="UTF-8") as file:
        data = json.load(file)

    data_dict = {}

    for dish in data["receipts"][0]["items"]:
        if dish["description"][-1].isdigit():
            description = dish["description"][:-1]
            amount = dish["description"][-1]
            if "гость" not in description.lower() and "итого" not in description.lower():
                if int(dish["description"][-1]) > 1:
                    unit_price = int(dish["amount"]) / int(dish["description"][-1])
                    data_dict.setdefault(description, round(unit_price))
                else:
                    unit_price = round(int(dish["amount"]))
                    data_dict.setdefault(description, unit_price)




    conn = sqlite3.connect("menu.db")

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY, Dish TEXT, Price INTEGER)")

    cursor.execute("SELECT COUNT(*) FROM menu")
    row_count = cursor.fetchone()[0]

    if row_count == 0:

        for key, value in data_dict.items():
            cursor.execute("INSERT INTO menu (Dish, Price) VALUES (?, ?)", (str(key), int(value)))

        conn.commit()

    conn.close()


def get_items():

    conn = sqlite3.connect("menu.db")

    cursor = conn.cursor()
    cursor.execute("SELECT Dish, Price FROM menu")
    items = cursor.fetchall()
    conn.close()

    return items


def get_price_dish(dish_name):

    conn = sqlite3.connect("menu.db")

    cursor = conn.cursor()
    cursor.execute("SELECT Price FROM menu WHERE Dish = ?", (dish_name, ))
    
    result = cursor.fetchone()
    
    
    return result[0]