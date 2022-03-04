import sqlite3
import logging
import pandas as pd

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
                columns = ['trans_type', 'client_name', 'item',
                    'quantity', 'price']
                df = pd.DataFrame(data=data, columns=columns)
                df.to_sql('transactions', self.con,
                    if_exists = 'append', index=False)
            except Exception as error:
                logging.error(" **Error writing to table: %s" % error)
