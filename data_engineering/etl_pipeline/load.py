from sqlalchemy import create_engine
import pandas as pd

class db_connection():
    def __init__(self):
        self.user = 'etl' # database login info
        self.password = 'pipeline'
        self.host = '127.0.0.1'
        self.database = 'pipeline_test'
        self.connect()

    def __del__(self):
        self.engine.dispose()

    # Using SQLAlchemy for pd.to_sql
    def connect(self):
        try: # pip install mysql-python-connector
            self.engine = create_engine(f'mysql+mysqlconnector://{self.user}:{self.password}@localhost/{self.database}')
        except ValueError as vx:
            print(vx)
        except Exception as ex:
            print(ex)

    def push_query(self, frame):
        tableName = 'tallest_buildings_metrics'
        try:
            df = frame.to_sql(tableName, self.engine, if_exists='fail')
        except ValueError as vx:
            print(vx)
        except Exception as ex:   
            print(ex)
        else:
            print(f"\t- Table {tableName} created successfully")

def load(frame):
    db = db_connection()
    return db.push_query(frame)