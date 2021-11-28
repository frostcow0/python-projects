import pandas as pd
import datatable as dt
from prefect import task, Flow, Parameter
from prefect.engine.state import State
from pandas import DataFrame
from timeit import Timer

from pyScripts.memory_reduction import reduce_memory_usage


def print_results(state:State) -> None:
    """ Helper function for displaying results of tasks. """
    for task, result in state.result.items():
        print(f'{task.name}: {result}')

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

@task
def reduce_mem(frame:DataFrame) -> DataFrame:
    return reduce_memory_usage(frame)

with Flow("test-data-flow-1") as flow:
    debug = Parameter("debug", default=0)
    df = import_data()
    p = print_frame_head(df, debug=debug, upstream_tasks=[df])
    minimized = reduce_mem(df)

def debug_flow() -> None:
    """ Runs flow in debug mode. """
    return flow.run(parameters=dict(debug=1))

def timed_flow(num:int) -> None:
    """ Times runtime of debug_flow. Takes number of iterations as an argument. """
    time = Timer('debug_flow()',
        'from __main__ import debug_flow'
        ).timeit(number=num)
    print(f'\nTimed flow took {time} seconds to run over {num} iterations.')

# state = flow.run()
state = debug_flow()
print_results(state)
# timed_flow(5)
