# Core Library
import io
import json
import urllib.request as rq
from typing import Any, Dict
from datetime import timedelta, date

# Third Party
import pandas as pd
import numpy as np
import prefect
from prefect import task, Flow
# from prefect.executors import LocalDaskExecutor
from prefect.run_configs import LocalRun
from prefect.core.parameter import Parameter
# from prefect.engine.results import LocalResult
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
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
PARAM_GRID = [
    {
        'activation': ['identity', 'logistic', 'tanh', 'relu'],
        'solver': ['lbfgs', 'sgd', 'adam'],
        'hidden_layer_sizes': [
            (1,),(2,),(3,),(4,),(5,),(6,),(7,),
            (8,),(9,),(10,),(11,),(12,),(13,),
            (14,),(15,),(16,),(17,),(18,),(19,),
            (20,),(21,)
        ],
        'max_iter': [600, 700, 800, 900, 1000]
    }
]
RANDOM_STATE = 2
DEFAULT_COUNTRY = "USA"
COVID_LATEST_DATA_URL = "https://covid.ourworldindata.org/data/latest/owid-covid-latest.json"
COVID_WHOLE_DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"
COVID_DATA_FILEPATH = "./data/raw-covid-whole-2021-12-04.json"
FLOW_NAME = "Covid analysis workflow"

def get_covid_df(url:str) -> pd.DataFrame:
    """Helper function for data extraction tasks"""
    with rq.urlopen(url) as url:
        covid_data = json.loads(url.read().decode())
        covid_df = pd.DataFrame(covid_data)
        return covid_df

@task#(max_retries=3, delay=timedelta(seconds=10)) # (result=LocalResult())
def extract_whole_covid_data() -> pd.DataFrame:
    """Download data via HTTP and create DataFrame"""
    return get_covid_df(COVID_WHOLE_DATA_URL)

@task
def extract_latest_covid_data() -> pd.DataFrame:
    """Download data via HTTP and create DataFrame"""
    return get_covid_df(COVID_LATEST_DATA_URL)

@task
def extract_covid_data_from_file() -> pd.DataFrame:
    """Return dataframe of data from JSON"""
    covid_df = pd.read_json(COVID_DATA_FILEPATH)
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
    data.to_json(f'./data/{type}-covid-{range}-{today}.json')

@task
def extract_full_country_data(data:pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe from the data dictionary nested in the covid data"""
    df = pd.DataFrame.from_dict(data.data)
    return df

@task
def extract_label_column(data:pd.DataFrame, column:str) -> pd.Series:
    """Create a copy of the column and return it as a Series"""
    series = data[column].copy().rename('')
    return series

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
def scale_data(X:pd.DataFrame) -> pd.DataFrame:
    """Uses StandardScaler to scale the data"""
    X = StandardScaler().fit_transform(X)
    X = pd.DataFrame(X)
    return X

@task
def check_data(data:Dict) -> None:
    """Checks train_test dict for NaN and infinite values"""
    for k in data:
        print(np.any(np.isnan(data[k])))
        print(np.all(np.isfinite(data[k])))
    return None

@task
def grid_search(data:Dict) -> None:
    """Uses GridSearchVC to hypertune parameters using MLPRegressor & PARAM_GRID"""
    reg = GridSearchCV(MLPRegressor(), PARAM_GRID,
        cv=3, scoring='neg_mean_absolute_error')
    reg.fit(data['X_train'], data['y_train'])
    print("Best parameters set found on development set:")
    print(reg.best_params_)
    return None

@task
def train_model(data:Dict) -> None:
    """Trains MLPRegressor"""
    reg = MLPRegressor(max_iter=1000)
    reg.fit(data['X_train'], data['y_train'])
    return None

def create_flow() -> Flow:
    """Creates and returns flow object"""
    # Haven't used different executors enough to know the difference
    with Flow(FLOW_NAME, run_config=LocalRun()) as flow:
        country = Parameter("country", default=DEFAULT_COUNTRY)

        # covid_df = extract_whole_covid_data()
        covid_df = extract_covid_data_from_file()
        filtered_covid_df = filter_data(covid_df, country)
        
        # Only for whole data, not latest
        full_df = extract_full_country_data(filtered_covid_df)

        base_y = extract_label_column(full_df, 'new_cases')
        cleaned_y = clean_NaN(base_y)
        # print_head(cleaned_y)

        base_X = remove_overfit_columns(full_df, DROP_COLUMNS)
        cleaned_X = clean_NaN(base_X)
        optimal_X = optimize_feature_columns(cleaned_X, 10, cleaned_y)
        scaled_X = scale_data(optimal_X)
        # print_head(scaled_X)

        train_test_data = split_data(scaled_X, cleaned_y)
        check_data(train_test_data)
        # check_for_infinity(train_test_data)

        # Some issue with my data's format & type while being processed
        # within the model.
        # Going back to Kaggle. Maybe I'm using the wrong model?
        # Just don't know enough yet.
        # train_model = grid_search(train_test_data)


        # save_data(covid_df, 'raw', 'whole')

    return flow

if __name__ == '__main__':
    flow = create_flow()
    flow.run()
