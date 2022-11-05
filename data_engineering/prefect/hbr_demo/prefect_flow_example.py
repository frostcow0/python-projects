import pandas as pd
from prefect import flow, task
import requests


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
def save_dataframe(df:pd.DataFrame, filename:str):
    """Saves the provided dataframe to a CSV with the provided filename.

    Args:
        df (pd.DataFrame): The dataframe to save as a CSV
        filename (str): The filename that the CSV will be called
    """
    df.to_csv(filename, index=False)

@flow
def covid_data(url:str, filename:str):
    """Gets json data from the provided url and formats it as
    a pandas dataframe before saving to a CSV with the provided filename.

    Args:
        url (str): The url to the json file/data
        filename (str): The filename that the CSV will be called
    """
    data = get_json_data(url)
    save_dataframe(data, filename)


if __name__ == "__main__":
    covid_data(url=OWID_COVID_URL, filename="covid.csv")
