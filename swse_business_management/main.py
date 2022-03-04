# Third Party
import logging

# Proprietary
from database import Database
from window import create_app

FILENAME = 'silly.db'
logging.basicConfig(level=logging.DEBUG)

def main():
    db = Database(FILENAME)
    transactions = db.get_transactions()
    create_app("SWSE BM", transactions, db)

if __name__ == '__main__':
    main()
