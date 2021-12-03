# Core Library
import io
import json
import urllib.request as rq
from typing import Any, Dict
from datetime import timedelta, date

# Third Party
import pandas as pd
import prefect
from prefect import task, Flow
# from prefect.executors import LocalDaskExecutor
from prefect.run_configs import LocalRun
from prefect.core.parameter import Parameter
# from prefect.engine.results import LocalResult
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


DEFAULT_COUNTRY = "USA"
# COVID_DATA_URL = "https://covid.ourworldindata.org/data/latest/owid-covid-latest.json"
COVID_DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"
FLOW_NAME = "Covid analysis workflow"


@task#(max_retries=3, delay=timedelta(seconds=10)) # (result=LocalResult())
def extract_covid_data() -> pd.DataFrame:
    """Download data via HTTP and create DataFrame"""
    with rq.urlopen(COVID_DATA_URL) as url:
        covid_data = json.loads(url.read().decode())
        covid_df = pd.DataFrame(covid_data)
        return covid_df

@task
def filter_data(covid_df:pd.DataFrame, country:str) -> pd.DataFrame:
    """Filter for the given country"""
    logger = prefect.context.get("logger")
    logger.info(f'Filtering data for country: {country}')
    filtered_df = covid_df[country].copy()
    return filtered_df

@task
def print_data(data:Any) -> None:
    """Only prints to the local output"""
    print(data)

@task
def print_columns(data:pd.DataFrame) -> None:
    """Prints columns of dataframe"""
    print([column for column in data.columns])

@task
def print_head(data:pd.DataFrame) -> None:
    """Print the head of a dataframe"""
    print(data.head())

@task
def save_data(data:pd.DataFrame, type:str, range:str) -> None:
    """Saves dataframe to csv. Ex. of type is filtered. Ex. of range is latest."""
    today = date.today()
    data.to_csv(f'./data/{type}-covid-latest-{today}.csv', index=False)

@task
def extract_full_country_data(data:pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(data.data)
    return df

@task
def extract_label_column(data:pd.DataFrame, column:str) -> pd.Series:
    return data.copy()[column]

@task
def clean_NaN(data:pd.DataFrame) -> pd.DataFrame:
    df = data.copy().fillna(0)
    return df

@task
def split_data(data:Dict) -> Dict:
    pass

def create_flow() -> Flow:
    """Creates and returns flow object"""
    # Haven't used different executors enough to know the difference
    with Flow(FLOW_NAME, run_config=LocalRun()) as flow:
        country = Parameter("country", default=DEFAULT_COUNTRY)

        covid_df = extract_covid_data()
        filtered_covid_df = filter_data(covid_df, country)
        print_head(filtered_covid_df)

        # Only for whole data, not latest
        full_df = extract_full_country_data(filtered_covid_df)
        # print_columns(full_df)

        label = extract_label_column(full_df, 'new_cases')
        label = clean_NaN(label)
        print_head(label)


        # save_data(filtered_covid_df, 'filtered', 'latest')

    return flow

if __name__ == '__main__':
    flow = create_flow()
    flow.run()
