import prefect
import pandas as pd
from timeit import Timer
import datatable as dt
from prefect import task, Flow, Parameter
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
def print_frame_head(frame:DataFrame, debug) -> None:
    if debug:
        print(frame.head())

@task # Not tested
def reduce_mem(frame:DataFrame) -> DataFrame:
    return reduce_memory_usage(frame)

with Flow("test-data-flow-1") as flow:
    debug = Parameter("debug", default=0)
    df = import_data()
    p = print_frame_head(df, debug=debug, upstream_tasks=[df])

def debug_flow():
    return flow.run(parameters=dict(debug=1))

# state = flow.run()
state = debug_flow()
print_results(state)

# time1 = Timer('run_flow()',
#     'from __main__ import run_flow'
#     ).timeit(number=1)
