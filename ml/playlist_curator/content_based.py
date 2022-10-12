# https://towardsdatascience.com/recommendation-systems-explained-a42fc60591ed

# Ideally I make either one class that can be passed a string to
# decide the distance method used, or I make a Super Class for the
# different potential methods

from math import pow
import pandas as pd
from typing import Tuple
from decimal import Decimal
from numpy import dot
from numpy.linalg import norm
from sklearn.preprocessing import OneHotEncoder


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

class CosineRecommend():
    """
    This class is for using the Cosine method of similarity
    to recommend n songs.
    """
    def __init__(self, saved_songs:pd.DataFrame):
        self.saved_songs = saved_songs

    def cosine_sim(self, v1:pd.Series, v2:pd.Series) -> int:
        """
        This function will calculate the cosine similarity between two vectors
        """
        d = dot(v1,v2)
        return d/(norm(v1)*norm(v2))

    def recommend(self, inputVec:pd.Series, n_rec:int):
        """
        inputVec (dataframe): The dataframe
        n_rec (int): amount of rec user wants
        """

        # calculate similarity of input book_id vector w.r.t all other vectors
        self.saved_songs['sim']= self.saved_songs.apply(
            lambda x: self.cosine_sim(inputVec, x.values), axis=1)

        # returns top n user specified songs
        return self.saved_songs.nlargest(columns='sim',n=n_rec)

class MinkowskiRecommend():
    """
    https://www.geeksforgeeks.org/minkowski-distance-python/

    This class is for using the Minkowski method of similarity
    to recommend n songs.
    """
    def __init__(self, saved_songs:pd.DataFrame):
        self.saved_songs = saved_songs

    def p_root(self, value:int, root:int) -> int:
        """
        Function distance between two points and
        calculate distance value to given root
        value (p is root value)
        """
        root_value = 1/float(root)
        return round(Decimal(value)**Decimal(root_value),3)

    def minkowski_distance(self, v1:pd.Series,
            v2:pd.Series, p_value:int) -> int:
        """
        Pass the p_root function to calculate all the value of
        vector parallelly.
        """
        return (
            self.p_root (sum (pow (abs(a-b),
            p_value) for a, b in zip(v1, v2)), p_value)
        )

    def recommend(self, inputVec:pd.Series, n_rec:int, p_value:int=2):
        """
        inputVec (dataframe): The dataframe
        n_rec (int): amount of rec user wants
        p (int): typically 1 or 2, corresponding to Manhattan
                    distance and Euclidean distance respectively
        """

        # calculate similarity of input song vector with
        # relation to all other vectors
        self.saved_songs['sim']= self.saved_songs.apply(
            lambda x: self.minkowski_distance(inputVec,
            x.values, p_value), axis=1)

        # returns top n user specified songs
        return self.saved_songs.nlargest(columns='sim',n=n_rec)

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
    # df = ohe(saved = df, enc_col = 'Album Release Date')
    # df = ohe(saved = df, enc_col = 'Explicit')
    # df = ohe(df = df, enc_col = 'Song Name')

    # df['track_id'], _ = pd.factorize(df['Track ID'])

    # drop redundant columns
    cols = ['Duration', 'Song Popularity', 'Album Release Date',
        'Song Name', 'Album Name', 'Artist Name', 'Explicit']
    df.drop(columns = cols, inplace = True)
    df.set_index('Track ID', inplace = True)

    # ran on a sample as an example
    t = df.copy()
    t.drop(columns=['Unnamed: 0'], inplace=True)
    print(t.head())
    cbr = CosineRecommend(saved_songs = t)
    # print(cbr.recommend(track_id = t.index[0], n_rec = 5))