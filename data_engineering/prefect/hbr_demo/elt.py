"""Author: Jon Martin - 11/4/2022"""

# Standard import
from os import listdir
from typing import List
# 3rd Party
import pandas as pd
import requests
import sqlalchemy
from prefect import flow, task


OWID_COVID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"

@task
def get_json_data(url:str) -> pd.DataFrame:
    """Uses requests to read the json file at the
    url provided, loads that json file, and returns it as a dataframe.

    Args:
        url (str): The url to the json file/data

    Returns:
        pd.DataFrame: The json file/data in pandas dataframe format
    """
    response = requests.get(url)
    return pd.DataFrame(response.json())

@task
def read_directory(directory:str) -> List[pd.DataFrame]:
    """Reads everything in the provided directory, appending
    CSVS, JSON, and Excel files to a list as pandas dataframes.

    Args:
        directory (str): The directory to look for files in

    Returns:
        List[pd.DataFrame]: List of dataframes read from the provided directory
    """
    data = []

    for file in listdir(directory):
        file_extension = file.split('.')[-1].lower()

        if file_extension == "json":
            data.append(pd.read_json(f"{directory}/{file}"))

        elif file_extension == "csv":
            data.append(pd.read_csv(f"{directory}/{file}"))

        elif file_extension in ("xlsx", "xls"):
            data.append(pd.read_excel(f"{directory}/{file}"))

    return data

@task
def prep_dataframe(data:pd.DataFrame) -> pd.DataFrame:
    """Transposes, keeps a subset of four columns, and drops the
    index of the provided dataframe before returning it.

    Args:
        data (pd.DataFrame): The pandas dataframe to alter

    Returns:
        pd.DataFrame: The altered dataframe
    """
    transposed = data.transpose()

    cols_to_keep = ['location', 'population', 'population_density', 'median_age']
    subset = transposed[cols_to_keep]

    subset.reset_index(drop=True, inplace=True)

    return subset

@task
def save_dataframe(directory:str, data:pd.DataFrame, filename:str):
    """Saves the provided dataframe to a CSV with the provided filename.

    Args:
        data (pd.DataFrame): The dataframe to save as a CSV
        filename (str): The filename that the CSV will be called
    """
    data.to_csv(f'{directory}/{filename}')

@task
def store_dataframe(data:pd.DataFrame, server:str, database:str, table:str):
    """Stores provided dataframe to the provided server & database at the
    provided table.

    Args:
        data (pd.DataFrame): Pandas dataframe to store in SQL
        server (str): Server to store the dataframe in
        database (str): Database to store the dataframe in
        table (str): Table name to store the dataframe in
    """
    # Not specifying user & password means it uses Window Authentication
    engine = sqlalchemy.create_engine(
        f"mssql+pyodbc://{server}/{database}?driver=SQL+Server",
        echo=False)

    with engine.connect() as connection:
        data.to_sql(
            name=table,
            con=connection,
            if_exists='replace')

@flow
def elt(directory:str="data", url:str=OWID_COVID_URL, filename:str="covid.csv", server:str="FETTUCCINE",
        database:str="prefect_demo", table:str="populus"):
    """Gets json data from the provided url and formats it as
    a pandas dataframe before saving to a CSV with the provided filename.

    Args:
        url (str): The url to the json file/data
        filename (str): The filename that the CSV will be called
    """
    # Gets COVID data from Our World in Data (OWID)
    data = get_json_data(url=url)
    # Saves the raw COVID data as a CSV
    save_dataframe(directory=directory, data=data, filename=filename)
    # Formats the COVID data for ease and usability
    prepped_data = prep_dataframe(data=data)
    # Stores the formatted COVID data to SQL
    store_dataframe(data=prepped_data, server=server, database=database, table=table)

    # Repeat the process for CSV, JSON, & Excel files in a given directory
    dir_data = read_directory(directory=directory)
    # This is called df and not data because you shouldn't reuse variable names

    #### This doesn't work yet, for some reason the data isn't reading in to the right format for prep_dataframe
    #### Need to use these funcs in notebook
    # for df in dir_data:
    #     prepped_df = prep_dataframe(data=df)
    #     store_dataframe(data=df, server=server, database=database, table=table)


if __name__ == "__main__":
    elt()
