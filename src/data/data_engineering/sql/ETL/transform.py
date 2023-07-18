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

    
    def data_modeling(self):
        return
    
    def save(self):
        self.joined_dataset.to_json('../data/interim/cleaned.jsonl', lines=True, orient='records')