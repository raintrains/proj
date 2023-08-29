import sqlite3

from data_parser_json import data_process_json


def create_db_dishes():

    data_dict = data_process_json("receipt.json")

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

# create_db_dishes()