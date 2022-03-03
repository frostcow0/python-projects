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
            self.con.close()

    def select_all_from_table(self, table:str) -> pd.DataFrame:
        """Selects * from specified table"""
        if self.con:
            query = f"SELECT * FROM {table}"
            try:
                df = pd.read_sql(query, self.con)
                return df
            except Exception as error:
                logging.error(" **Error reading from table: %s" % error)

    def store_data(self, data:pd.DataFrame, table:str) -> None:
        """Stores the DataFrame at the specified table"""
        if self.con:
            try:
                result = data.to_sql(table, self.con,
                    if_exists = 'append', index=False)
                return result
            except Exception as error:
                logging.error(" **Error reading from table: %s" % error)
            