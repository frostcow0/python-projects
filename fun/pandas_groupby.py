import mysql.connector
from mysql.connector import errorcode
import pandas as pd

class db_connection():
    def __init__(self, query):
        self.user = 'etl' # database login info
        self.password = 'pipeline'
        self.host = '127.0.0.1'
        self.database = 'sakila'
        self.query = query
        self.connect()

    def __del__(self):
        self.connection.close()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.database
            )
            self.cursor = self.connection.cursor()
            print(f'\t- Connection Initialized for {self.database}')
        except mysql.connector.Error as err:
            if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
                print('\t- Invalid Credentials')
            elif err.errno==errorcode.ER_BAD_DB_ERROR:
                print('\t- Database not found')
            else:
                print('\t- Cant connect to database: ',err)

    def pull_query(self):
        self.cursor.execute(self.query)
        self.columns = [i[0] for i in self.cursor.description]
        return pd.DataFrame(self.cursor.fetchall(),
                columns = self.columns)

def extract():
    db = db_connection('select * from tallest_buildings')
    return db.pull_query()

# bldg_name, city, country, stories, year, height_m

df = extract()

# Unique cities sorted by building with the most stories
city_stories = df.groupby('city')['stories'].max().sort_values(ascending=False)

# Unique cities sorted by tallest building, with building info
city_height = df.groupby('city').apply(lambda df: df.loc[df['height_m'].idxmax()])

country_avg_height = df.groupby('country')['height_m'].mean()

print("-"*60)
print(df.head())
print("-"*60)
print(city_stories.head())
print("-"*60)
print(city_height.head())
print("-"*60)
print(country_avg_height.head())