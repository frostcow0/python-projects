# Third Party
import logging
import pandas as pd

# Proprietary
from database import Database
from window import create_app

FILENAME = 'silly.db'
TABLENAME = 'inventory'
logging.basicConfig(level=logging.DEBUG)

def main():
    db = Database(FILENAME)
    inventory = db.get_inventory()
    transactions = db.get_transactions()
    data = {
        "inventory": inventory,
        "transactions": transactions
    }
    create_app("SWSE BM", data, db)
    pass

def silly_store():
    db = Database(FILENAME)
    data = {
        "item": ['spice', 'deathsticks'],
        "amount": [400, 50],
        "unit": ['lbs', 'sticks']
    }
    df = pd.DataFrame(data)
    result = db.store_data(df, TABLENAME)
    print(df.head())
    print(result)

def silly_read():
    db = Database(FILENAME)
    df = db.select_all_from_table(TABLENAME)
    print(df.head())

if __name__ == '__main__':
    main()
    # silly_store()
    # silly_read()
