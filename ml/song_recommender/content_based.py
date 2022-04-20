# https://towardsdatascience.com/recommendation-systems-explained-a42fc60591ed

import pandas as pd
from typing import Tuple
from numpy import dot
from numpy.linalg import norm
from sklearn.preprocessing import OneHotEncoder # my addition


def normalize(data) -> list:
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

def ohe(saved:pd.DataFrame, last:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    '''
    This function will one hot encode the specified columns and add it back
    onto the input dataframes. These have to be done together to avoid
    dataframe shape issues (different unique values make unexpected columns).
    
    params:
        saved (DataFrame) : The dataframe containing user's saved songs
        last (DataFrame) : The dataframe containing user's recently played songs
    
    returns:
        A tuple of the dataframes with OHE columns replacing the originals
    '''
    # Categorical columns to One-hot Encode
    cat_cols = ["Album Release Date", "Explicit"]
    # Ignore is what allows us to have consistent dataframe shapes
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    # Order is important here, last has to be fit before saved
    ohe_df_l = pd.DataFrame(OH_encoder.fit_transform(last[cat_cols]))
    ohe_df_s = pd.DataFrame(OH_encoder.transform(saved[cat_cols]))
    # OHE loses index, so we re-apply (according to my Udemy notes)
    ohe_df_l.index = last.index
    ohe_df_s.index = saved.index
    # Drop the original categorical columns
    last.drop(cat_cols, axis=1, inplace=True)
    saved.drop(cat_cols, axis=1, inplace=True)
    return (
        pd.concat([saved, ohe_df_s], axis = 1),
        pd.concat([last, ohe_df_l], axis = 1),
    )

class CBRecommend():
    def __init__(self, df):
        self.df:pd.DataFrame = df
        
    def cosine_sim(self, v1,v2):
        '''
        This function will calculate the cosine similarity between two vectors
        '''
        d = dot(v1,v2)
        return d/(norm(v1)*norm(v2))
    
    def recommend(self, inputVec, n_rec):
        """
        df (dataframe): The dataframe
        song_id (string): Representing the song name
        n_rec (int): amount of rec user wants
        """
        
        # calculate similarity of input book_id vector w.r.t all other vectors
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
