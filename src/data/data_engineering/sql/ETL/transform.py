import pandas as pd
import os

class Transform():
    def __init__(self, joined_dataset):
        self.joined_dataset = joined_dataset

    def cleaning(self):
        # removing movie duplicates
        self.joined_dataset.drop_duplicates(subset=['title'], inplace=True)

        # removing NaN
        self.joined_dataset.dropna(inplace=True)

        # removing garbage from "year"
        self.joined_dataset['year'] = self.joined_dataset['year'].apply(lambda x: x.replace("I", ""))
        self.joined_dataset['year'] = self.joined_dataset['year'].apply(lambda x: x.replace("II", ""))
        self.joined_dataset['year'] = self.joined_dataset['year'].apply(lambda x: x.replace("III", ""))
        self.joined_dataset['year'] = self.joined_dataset['year'].apply(lambda x: x.replace("V", ""))
        self.joined_dataset['year'] = self.joined_dataset['year'].apply(lambda x: x.replace("X", ""))
        self.joined_dataset['year'] = self.joined_dataset['year'].apply(lambda x: x.strip())
    
    def save(self, output_path):
        self.joined_dataset.to_json(os.path.join(output_path, 'cleaned.jsonl'), lines=True, orient='records')