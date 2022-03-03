# Third Party
import logging
import pandas as pd

# Proprietary
from database import Database
from window import create_app

FILENAME = 'silly.db'
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

if __name__ == '__main__':
    main()
    # silly_store()
    # silly_read()
