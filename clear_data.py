import os
import shutil

def refresh_bot():

    photos_path = r"photos"
    customer_database_path = r"customer_account.db"
    menu_path = r"menu.db"
    receipt_path = r"receipt1.json"


    try:
        shutil.rmtree(photos_path)
        os.remove(customer_database_path)
        os.remove(menu_path)
        os.remove(receipt_path)
    except:
        pass