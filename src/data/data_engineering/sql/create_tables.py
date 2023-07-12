import psycopg2
import logging
import os

from dotenv import load_dotenv


load_dotenv()
 
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('USER')
DB_PASS = os.getenv('PASS')

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS)
    
    print("Database connected successfully")
    cur = conn.cursor()
    query_sql = """
    CREATE TABLE IF NOT EXISTS RATINGS(test integer, test2 integer)
    """
    cur.execute(query_sql)
    cur.close()
    conn.commit()
except:
    print("Database not connected successfully")

