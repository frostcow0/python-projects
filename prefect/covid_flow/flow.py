# Core Library
import io
import json
import urllib.request as rq
from typing import Any, Dict
from datetime import timedelta

# Third Party
import pandas as pd
import prefect
from prefect import task, Flow
# from prefect.executors import LocalDaskExecutor
from prefect.run_configs import LocalRun
from prefect.core.parameter import Parameter
# from prefect.engine.results import LocalResult


DEFAULT_COUNTRY = "USA"
COVID_DATA_URL = "https://covid.ourworldindata.org/data/latest/owid-covid-latest.json"
# https://covid.ourworldindata.org/data/owid-covid-data.json
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

def create_flow() -> Flow:
    """Creates and returns flow object"""
    # Haven't used different executors enough to know the difference
    with Flow(FLOW_NAME, run_config=LocalRun()) as flow:
        country = Parameter("country", default=DEFAULT_COUNTRY)

        covid_df = extract_covid_data()
        filtered_covid_df = filter_data(covid_df, country)

        print_data(filtered_covid_df)

    return flow

if __name__ == '__main__':
    flow = create_flow()
    flow.run()
