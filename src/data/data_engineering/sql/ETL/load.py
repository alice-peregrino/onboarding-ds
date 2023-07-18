import sqlalchemy as db
from tqdm import tqdm

class Load:
    def __init__(self, cleaned_data):
        self.cleaned_data = cleaned_data

    def insert_to_postgres(self):
        engine = db.create_engine("postgresql+psycopg2://postgres:5Sx!Pnn0@localhost:5432/imdb")
        conn = engine.connect()
        metaData = db.MetaData(schema="public")
        metaData.reflect(bind=conn)

        columns = ['title', 'year', 'duration', 'rating', 'gross']
        df_movieratings = self.cleaned_data[columns]
        list_values = []
        table_movieratings = metaData.tables['public.movieratings']
        for index, row in tqdm(df_movieratings.iterrows()):
            values = {
                'movie_title': row['title'],
                'movie_year': row['year'],
                'movie_duration': row['duration'],
                'movie_gross': row['gross'],
                'movie_rating': row['rating']
                }
            list_values.append(values) 
        query = db.insert(table_movieratings)
        res = conn.execute(query, list_values)
        conn.commit()

        list_directors = self.cleaned_data['directors'].tolist()
        list_directors = [d for director in list_directors for d in director.split(', ')]
        set_directors = set(list_directors)
        dict_directors = {'director_name': list(set_directors)}
        df_directors = pd.DataFrame(dict_directors)
        list_values = []
        table_moviedirectors = metaData.tables['public.moviedirectors']
        for index, row in tqdm(df_directors.iterrows()):
            values = {
                'director_name': row['director_name']
                }
            list_values.append(values)

        query = db.insert(table_moviedirectors)
        res = conn.execute(query, list_values)
        conn.commit()
        
        list_stars = self.cleaned_data['stars'].tolist()
        list_stars = [s for star in list_stars for s in star.split(', ')]
        set_stars = set(list_stars)
        dict_stars = {'star_name': list(set_stars)}
        df_stars = pd.DataFrame(dict_stars)
        list_values = []
        table_moviestars = metaData.tables['public.moviestars']
        for index, row in tqdm(df_stars.iterrows()):
            values = {
                'star_name': row['star_name']
                }
            list_values.append(values)
        query = db.insert(table_moviestars)
        res = conn.execute(query, list_values)
        conn.commit()

        list_genres = self.cleaned_data['genre'].tolist()
        list_genres = [g for genre in list_genres for g in genre.split(', ')]
        set_genres = set(list_genres)
        dict_genres = {'genre_name': list(set_genres)}
        df_genres = pd.DataFrame(dict_genres)
        list_values = []
        table_moviegenres = metaData.tables['public.moviegenres']
        for index, row in tqdm(df_genres.iterrows()):
            values = {
                'genre_name': row['genre_name']
                }
            list_values.append(values)
        query = db.insert(table_moviegenres)
        res = conn.execute(query, list_values)
        conn.commit()

        list_classification = self.cleaned_data['classification'].tolist()
        set_classification = set(list_classification)
        dict_classification = {'classification_name': list(set_classification)}
        df_classification = pd.DataFrame(dict_classification)
        list_values = []
        table_movieclassification = metaData.tables['public.movieclassification']
        for index, row in tqdm(df_classification.iterrows()):
            values = {
                'classification_id': row['classification_id'],
                'classification_name': row['classification_name']
                }
            list_values.append(values)
        query = db.insert(table_movieclassification)
        res = conn.execute(query, list_values)
        conn.commit()