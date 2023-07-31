import sqlite3

def create_db_clients():

    conn = sqlite3.connect("customer_account.db")
    curssor = conn.cursor()
    curssor.execute("CREATE TABLE IF NOT EXISTS customer_account (id INTEGER PRIMARY KEY, Name TEXT, Amount INTEGER)")

    conn.commit()
    conn.close()

def update_db_clients(Name, Amount):

    conn = sqlite3.connect("customer_account.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customer_account (Name, Amount) VALUES (?, ?)", (str(Name), int(Amount)))

    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect("customer_account.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Name, Amount FROM customer_account")
    items = cursor.fetchall()
    conn.commit()
    conn.close()

    return items