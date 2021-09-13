import pandas as pd
import extract as e
import transform as t

if __name__ == '__main__':
    try:
        data = e.extract()
        transf = t.transform(data)
        print(transf.head())
    except:
        print('Couldn\'t run extract.py')