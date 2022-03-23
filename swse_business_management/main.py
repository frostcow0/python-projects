# Third Party
import logging

# Proprietary
from database import Database
from window import create_app


FILENAME = "swsebm.db"
logging.basicConfig(level=logging.INFO) # swap to DEBUG

def main():
    db = Database(FILENAME)
    create_app("SWSE BM", db)

def example():
    db = Database("silly.db")
    create_app("Example DB", db)

if __name__=="__main__":
    main()
    # example()
