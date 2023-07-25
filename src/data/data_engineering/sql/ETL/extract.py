import pandas as pd
import os

class Extract():
    def __init__(self, data_paths = []):
        self.data_paths = data_paths
        self.joined_data = pd.DataFrame()

    def extract(self):
        for path in self.data_paths:
            temp = pd.read_json(path, lines=True)
            self.joined_data = pd.concat([self.joined_data, temp])

    def save(self, output_path):
        self.joined_data.to_json(os.path.join(output_path, 'output.jsonl'), lines=True, orient='records')