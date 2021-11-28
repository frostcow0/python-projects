from timeit import Timer
import datatable as dt
import pandas as pd


# Claims that it is 50x faster on millions of rows
def test_datatable():
    frame = dt.fread(r'./data/sample_in.csv').to_pandas()
    dt.Frame(frame).to_csv('./data/sample_out.csv')

def test_pandas():
    frame = pd.read_csv(r'./data/sample_in.csv')
    frame.to_csv(r'./data/sample_out.csv')

time1 = Timer('test_datatable()', 'from __main__ import test_datatable').timeit(number=1)
time2 = Timer('test_pandas()', 'from __main__ import test_pandas').timeit(number=1)

print(f'It took {time1} seconds for datatable to read from csv then write to csv.')
print(f'It took {time2} seconds for pandas to read from csv then write to csv.')