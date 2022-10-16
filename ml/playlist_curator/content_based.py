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
from abc import ABC, abstractmethod


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

def p_root(value:int, root:int) -> int:
    """Calculate distance from value to root.

    Args:
        value (int): Some number
        root (int): The p value in Minkowski distance

    Returns:
        int: The distance from the value to the root
    """
    root_value = 1 / float(root)
    return round(Decimal(value) ** Decimal(root_value), 3)

    # Should I implement pytest...?
class Recommender(ABC):
    """Super class for recommender methods."""

    @abstractmethod
    def measure_distance(self, vector_1:pd.Series, vector_2:pd.Series) -> float:
        """Measures distance between vectors using some methodology."""

    def recommend(self, goal_vector:pd.Series, comparison_set:pd.DataFrame,
            n_rec:int) -> pd.DataFrame:
        """Sorts the comparison_set by the rows' similarity to
        the goal_vector and returns the comparison_set.

        Args:
            goal_vector (pd.Series): The vector by which we rank the comparison_set
            comparison_set (pd.DataFrame): Set of vectors (rows) that we rank based on
                similarity to the goal_vector
            n_rec (int): The number of vectors from the comparison_set to return

        Returns:
            pd.DataFrame: Top (n_rec) vectors from the comparison_set ranked by
                their similarity to the goal_vector
        """
        # calculate similarity of goal_vector w.r.t all other vectors
        comparison_set['sim']= comparison_set.apply(
            lambda x: self.measure_distance(goal_vector, x.values), axis=1)

        # Converts to number format, sometimes throws an error using nlargest otherwise
        comparison_set['sim'] = pd.to_numeric(comparison_set['sim'], errors='coerce')

        # returns top n user specified vectors
        return comparison_set.nlargest(columns='sim',n=n_rec)

class CosineDistance(Recommender):
    """Recommender subclass implementing Cosine Distance as a
    measure of similarity."""

    def measure_distance(self, vector_1:pd.Series, vector_2:pd.Series) -> float:
        """Measures distance between vectors using Cosine Distance.

        Args:
            vector_1 (pd.Series): Vector of numbers
            vector_2 (pd.Series): Vector of numbers

        Returns:
            float: Cosine distance between the vectors
        """
        product = dot(vector_1,vector_2)
        return product / (norm(vector_1) * norm(vector_2))

class MinkowskiDistance(Recommender):
    """Recommender subclass implementing Minkowski Distance as a
    measure of similarity.

    https://www.geeksforgeeks.org/minkowski-distance-python/"""
    def __init__(self, p_value:int) -> None:
        self.p_value = p_value

    def measure_distance(self, vector_1: pd.Series, vector_2: pd.Series) -> float:
        """Measures distance between vectors using Minkowski Distance.

        Args:
            vector_1 (pd.Series): Vector of numbers
            vector_2 (pd.Series): Vector of numbers

        Returns:
            float: Minkowski distance between the vectors
        """
        return (
            p_root(sum (pow (abs(a - b), self.p_value)
                for a, b in zip(vector_1, vector_2)), self.p_value)
        )


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