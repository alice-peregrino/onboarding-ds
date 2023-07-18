import psycopg2
import os
import logging
from tqdm import tqdm

from dotenv import load_dotenv

load_dotenv()

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
 
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('USER')
DB_PASS = os.getenv('PASS')

# try:
conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS)
    
logging.info("Database connected successfully")
cur = conn.cursor()
query_sql = (
        """
        CREATE TABLE MovieRatings (
            movie_id SERIAL PRIMARY KEY,
            movie_title VARCHAR(255) UNIQUE NOT NULL,
            movie_year INTEGER NOT NULL,
            movie_duration INTEGER NOT NULL,
            movie_gross FLOAT NOT NULL,
            movie_rating FLOAT NOT NULL
        )
        """,
        """ CREATE TABLE MovieDirectors (
                director_id SERIAL PRIMARY KEY,
                director_name VARCHAR(100) NOT NULL
                )
        """,
        """ CREATE TABLE MovieStars (
                star_id SERIAL PRIMARY KEY,
                star_name VARCHAR(100) NOT NULL
                )
        """,
        """ CREATE TABLE MovieGenres (
                genre_id SERIAL PRIMARY KEY,
                genre_name VARCHAR(40) NOT NULL
                )
        """,
        """ CREATE TABLE MovieClassification (
                classification_id SERIAL PRIMARY KEY,
                classification_name VARCHAR(20) NOT NULL
                )
        """)

for query in tqdm(query_sql):  
    cur.execute(query)

logging.info("Tables created sucessfully!")

cur.close()
conn.commit()

# except:
#     logging.info("Error in tables creation.")
