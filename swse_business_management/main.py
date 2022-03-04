# Third Party
import logging

# Proprietary
from database import Database
from window import create_app


FILENAME = "swsebm.db"
logging.basicConfig(level=logging.INFO) # swap to DEBUG

def main():
    db = Database(FILENAME)
    transactions = db.get_transactions()
    create_app("SWSE BM", transactions, db)

def example():
    db = Database("silly.db")
    transactions = db.get_transactions()
    create_app("Example DB", transactions, db)

if __name__=="__main__":
    main()
    # example()
