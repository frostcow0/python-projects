import pandas as pd
import extract as e
import transform as t
import load as l

if __name__ == '__main__':
    print('='*60)
    data = e.extract()
    print('-'*60)
    print('\t- Extracted Query')
    transf = t.transform(data)
    print('-'*60)
    print('\t- Transformed Data')
    print('-'*60)
    load = l.load(transf)
    print('='*60)