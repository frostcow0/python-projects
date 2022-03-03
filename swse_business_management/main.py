# Third Party
import logging
from venv import create
import pandas as pd

# Proprietary
from database import Database
from window import create_app

FILENAME = 'silly.db'
TABLENAME = 'inventory'
logging.basicConfig(level=logging.DEBUG)

def main():
    db = Database(FILENAME)
    inventory = db.select_all_from_table('inventory')
    data = {
        "inventory": inventory
    }
    create_app("SWSE BM", data)
    pass

def silly_store():
    db = Database(FILENAME)
    data = {
        "name": ['spice', 'deathsticks'],
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
