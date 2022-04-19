# https://towardsdatascience.com/recommendation-systems-explained-a42fc60591ed

import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm

def normalize(data):
    '''
    This function will normalize the input data to be between 0 and 1
    
    params:
        data (List) : The list of values you want to normalize
    
    returns:
        The input data normalized between 0 and 1
    '''
    min_val = min(data)
    if min_val < 0:
        data = [x + abs(min_val) for x in data]
    max_val = max(data)
    return [x/max_val for x in data]

def ohe(df, enc_col):
    '''
    This function will one hot encode the specified column and add it back
    onto the input dataframe
    
    params:
        df (DataFrame) : The dataframe you wish for the results to be appended to
        enc_col (String) : The column you want to OHE
    
    returns:
        The OHE columns added onto the input dataframe
    '''
    
    ohe_df = pd.get_dummies(df[enc_col])
    ohe_df.reset_index(drop = True, inplace = True)
    return pd.concat([df, ohe_df], axis = 1)

class CBRecommend():
    def __init__(self, df):
        self.df:pd.DataFrame = df
        
    def cosine_sim(self, v1,v2):
        '''
        This function will calculate the cosine similarity between two vectors
        '''
        d = dot(v1,v2)
        return d/(norm(v1)*norm(v2))
    
    def recommend(self, track_id, n_rec):
        """
        df (dataframe): The dataframe
        song_id (string): Representing the song name
        n_rec (int): amount of rec user wants
        """
        
        # calculate similarity of input book_id vector w.r.t all other vectors
        inputVec = self.df.loc[track_id].values
        self.df['sim']= self.df.apply(lambda x: self.cosine_sim(inputVec, x.values), axis=1)

        # returns top n user specified books
        return self.df.nlargest(columns='sim',n=n_rec)

if __name__ == '__main__':
    # constants
    PATH = 'song_recommender/data/data.csv'

    # import data
    df = pd.read_csv(PATH)

    # normalize the num_pages, ratings, price columns
    df['duration_norm'] = normalize(df['Duration'].values)
    df['song_popularity'] = normalize(df['Song Popularity'].values)
    # df['book_price_norm'] = normalize(df['book_price'].values)
    
    # OHE on publish_year and genre
    df = ohe(df = df, enc_col = 'Album Release Date')
    df = ohe(df = df, enc_col = 'Explicit')
    # df = ohe(df = df, enc_col = 'Song Name')

    # df['track_id'], _ = pd.factorize(df['Track ID'])
    
    # drop redundant columns
    cols = ['Duration', 'Song Popularity', 'Album Release Date', 'Song Name', 'Album Name', 'Artist Name', 'Explicit']
    df.drop(columns = cols, inplace = True)
    df.set_index('Track ID', inplace = True)
    
    # ran on a sample as an example
    t = df.copy()
    t.drop(columns=['Unnamed: 0'], inplace=True)
    print(t.head())
    cbr = CBRecommend(df = t)
    print(cbr.recommend(track_id = t.index[0], n_rec = 5))
