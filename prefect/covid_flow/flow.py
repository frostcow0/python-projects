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
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.neural_network import MLPRegressor


DROP_COLUMNS = [
    'date',
    'new_cases',
    'new_cases_per_million',
    'new_cases_smoothed',
    'new_cases_smoothed_per_million',
    'tests_units'
]
RANDOM_STATE = 2
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
def print_info(data:pd.DataFrame) -> None:
    """Print the info method of a dataframe"""
    print(data.info())

@task
def save_data(data:pd.DataFrame, type:str, range:str) -> None:
    """Saves dataframe to csv. Ex. of type is filtered. Ex. of range is latest."""
    today = date.today()
    data.to_csv(f'./data/{type}-covid-{range}-{today}.csv', index=False)

@task
def extract_full_country_data(data:pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe from the data dictionary nested in the covid data"""
    df = pd.DataFrame.from_dict(data.data)
    return df

@task
def extract_label_column(data:pd.DataFrame, column:str) -> pd.Series:
    """Create a copy of the column and return it as a Series"""
    return data.copy()[column]

@task
def optimize_feature_columns(X:pd.DataFrame, num_features:int, y:pd.Series) -> pd.DataFrame:
    """Create a copy of the columns and return them as a dataframe"""
    feature_selection = SelectKBest(score_func=f_regression, k=num_features)
    X_selected = feature_selection.fit_transform(X.copy(), y)
    X_selected = pd.DataFrame(X_selected)
    return X_selected

@task
def remove_overfit_columns(data:pd.DataFrame, columns:list) -> pd.DataFrame:
    """Removes columns that might cause overfit, such as the per million and smoothed versions of our label"""
    data = data.copy().drop(columns = columns)
    return data

@task
def clean_NaN(data:pd.DataFrame) -> pd.DataFrame:
    df = data.copy().fillna(0)
    return df

@task
def split_data(X:pd.DataFrame, y:pd.Series) -> Dict:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=RANDOM_STATE
    )
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test}

@task
def scale_data(data:Dict) -> Dict:
    """Uses StandardScaler to scale the data"""
    scaler = StandardScaler()
    scaler.fit(data['X_train'])
    for k, v in data.items():
        data[k] = scaler.transform(v)
    return data

@task
def train_model(data:Dict) -> MLPRegressor:
    """Trains MLPRegressor"""
    model = MLPRegressor(
        random_state=RANDOM_STATE,
        max_iter=500,
        learning_rate_init=0.1
    ).fit(data['X_train'], data['y_train'])
    return model

def create_flow() -> Flow:
    """Creates and returns flow object"""
    # Haven't used different executors enough to know the difference
    with Flow(FLOW_NAME, run_config=LocalRun()) as flow:
        country = Parameter("country", default=DEFAULT_COUNTRY)

        covid_df = extract_covid_data()
        filtered_covid_df = filter_data(covid_df, country)

        # Only for whole data, not latest
        full_df = extract_full_country_data(filtered_covid_df)

        base_y = extract_label_column(full_df, 'new_cases')
        cleaned_y = clean_NaN(base_y)
        print_head(cleaned_y)

        base_X = remove_overfit_columns(full_df, DROP_COLUMNS)
        cleaned_X = clean_NaN(base_X)
        optimal_X = optimize_feature_columns(cleaned_X, 10, cleaned_y)
        print_head(optimal_X)

        train_test_data = split_data(optimal_X, cleaned_y)
        scaled_data = scale_data(train_test_data)

        trained_model = train_model(scaled_data)


        # save_data(filtered_covid_df, 'filtered', 'latest')

    return flow

if __name__ == '__main__':
    flow = create_flow()
    flow.run()
