import sqlite3
import logging
import pandas as pd
from datetime import datetime, timedelta


class Database:
    """Database object for handling context"""
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)

    def __exit__(self) -> None:
        """Closes connection"""
        if self.con:
            self.con.commit()
            self.con.close()

    def select_all_from_table(self, table:str) -> pd.DataFrame:
        """Selects * from specified table"""
        if self.con:
            query = f"SELECT * FROM {table}"
            try:
                df = pd.read_sql(query, self.con)
                logging.debug(" Successfully read from %s" % table)
                return df
            except Exception as error:
                logging.error(" **Error reading from table: %s" % error)

    def get_inventory(self) -> pd.DataFrame:
        """Selects * from inventory"""
        if self.con:
            query = f"SELECT * FROM inventory"
            try:
                df = pd.read_sql(query, self.con)
                logging.debug(" Successfully read from inventory")
                return df
            except Exception as error:
                logging.error(" **Error reading from table: %s" % error)
    
    def get_transactions(self) -> pd.DataFrame:
        """Selects * from transactions"""
        if self.con:
            query = f"SELECT * FROM transactions"
            try:
                df = pd.read_sql(query, self.con)
                logging.debug(" Successfully read from transactions")
                return df
            except Exception as error:
                logging.error(" **Error reading from table: %s" % error)

    def get_current_session_id(self) -> int:
        """Selects current session_id from sessions table"""
        if self.con:
            query = "SELECT session_id as id FROM sessions WHERE session_date = DATE()"
            try:
                df = pd.read_sql(query, self.con)
                if df.empty:
                    date = pd.read_sql("SELECT MAX(session_date) as date from sessions", self.con)
                    date = datetime.strptime(date["date"][0], "%Y-%m-%d").date()
                    if datetime.now().date()-date == timedelta(days=7):
                        self.new_session()
                        logging.debug(" It's been seven days, getting a new session id")
                        return self.get_current_session_id()
                    else:
                        id = pd.read_sql("SELECT MAX(session_id) as id from sessions", self.con)
                        logging.debug(" In between sessions, using %i as session id" % id["id"][0])
                        return id["id"][0]
                else:
                    logging.debug(" Current session id is %i" % df["id"][0])
                    return df["id"][0]
            except Exception as error:
                logging.error(" **Error reading from table: %s" % error)


    def store_data(self, data:pd.DataFrame, table:str) -> None:
        """Stores the DataFrame at the specified table"""
        if self.con:
            try:
                data.to_sql(table, self.con,
                    if_exists = 'append', index=False)
            except Exception as error:
                logging.error(" **Error writing to table: %s" % error)

    def store_transaction(self, data:list) -> None:
        """Stores the data in transactions"""
        if self.con:
            try:
                columns = ['session_id', 'trans_type', 'client_name', 'item',
                    'quantity', 'price']
                data[0].insert(0, self.get_current_session_id())
                logging.debug(" Received transaction data: %s " % data)
                df = pd.DataFrame(data=data, columns=columns)
                df.to_sql('transactions', self.con,
                    if_exists = 'append', index=False)
            except Exception as error:
                logging.error(" **Error writing to table: %s" % error)

    def new_session(self) -> None:
        """Creates a new session"""
        if self.con:
            try:
                data = [datetime.today().strftime("%Y-%m-%d")]
                df = pd.DataFrame(data=[data], columns=["session_date"])
                df.to_sql("sessions", self.con,
                    if_exists = "append", index=False)
            except Exception as error:
                logging.error(" **Error creating session: %s" % error)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    db = Database("swsebm.db")
    # db.new_session()
    print(db.select_all_from_table("transactions"))
    # print(db.get_current_session_id())

    # ADD HUSTLE FEES
    # ADD DRUG PRICE CALCULATOR
