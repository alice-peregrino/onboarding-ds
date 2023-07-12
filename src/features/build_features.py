import pandas as pd
from typing import List

class FeatureExtractor():

    def __init__(self, 
                 dataframe: pd.DataFrame, 
                 cols_to_drop: List[str]):
        
        self.dataframe = dataframe
        self.cols_to_drop = cols_to_drop
        self.output_path = '../data/processed/features.csv'

    def remove_cols(self):
        self.dataframe.drop(columns=self.cols_to_drop, inplace=True)
    
    def encode_genre_col(self):
        dummies = pd.get_dummies(self.dataframe['genre'])

        genres = self.dataframe.genre.tolist()
        genres = [g for genre in genres for g in genre.split(', ')]

        atom_col = list(set(genres))

        for col in atom_col:
            self.dataframe[col] = dummies[[c for c in dummies.columns if col in c]].sum(axis=1)

    def encode_classification_col(self):
        classifications_dict = {
            'R': 1,
            'PG': 1, 
            'PG-13': 1, 
            'G': 2, 
            'Passed': 1, 
            'Not Rated': 0, 
            'Approved': 1, 
            '13+': 1,
            'TV-14': 1, 
            'TV-MA': 0, 
            'NC-17': 0, 
            'TV-PG': 2, 
            'GP': 2, 
            '12': 1, 
            'TV-G': 2, 
            '16+': 1,
            '10': 1, 
            '14': 1, 
            'Livre': 2, 
            'MA-17': 1, 
            'TV-Y7': 2, 
            '16': 1, 
            'M/PG': 1, 
            '18': 0, 
            'M': 1,
            '18+': 0, 
            'TV-Y7-FV': 1, 
            'TV-13': 1, 
            'X': 0
        }
        
        self.dataframe['classification'] = self.dataframe['classification'].apply(lambda x: classifications_dict[x])
    
    def save_data(self):
        self.dataframe.to_csv(self.output_path, index=False)
