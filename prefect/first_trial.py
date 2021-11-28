import prefect
import pandas as pd
from timeit import Timer
import datatable as dt
from prefect import task, Flow
from prefect.engine.state import State
from pandas import DataFrame

from pyScripts.memory_reduction import reduce_memory_usage


def print_results(state:State) -> None:
    """ Helper function for displaying results of tasks. """
    for task, result in state.result.items():
        print(f'{task.name}: {result}')

@task
def howdy_task():
    logger = prefect.context.get("logger")
    logger.info("Howdy partner!")

@task
def convert_type_1(frame:DataFrame) -> DataFrame:
    for column in frame.columns:
        frame[column] = pd.to_numeric(
            frame[column],
            errors = 'ignore'
        )
    return frame

@task
def import_data() -> DataFrame:
    filepath = r'./data/sample_out.csv'
    data = dt.fread(filepath).to_pandas()
    data.drop(columns = ['C0'], inplace=True) # Extra index
    return data

@task
def print_frame_head(frame:DataFrame) -> None:
    print(frame.head())

@task # Not tested
def reduce_mem(frame:DataFrame) -> DataFrame:
    return reduce_memory_usage(frame)

with Flow("test-data-flow-1") as flow:
    df = import_data()
    p = print_frame_head(df, upstream_tasks=[df])

    # print(type(df))
    # head = df.head()
    # print(head)

def run_flow():
    state = flow.run()

state = flow.run()
print_results(state)

# time1 = Timer('run_flow()',
#     'from __main__ import run_flow'
#     ).timeit(number=1)
