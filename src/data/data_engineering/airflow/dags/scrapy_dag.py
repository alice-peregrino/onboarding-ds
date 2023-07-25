import sys

sys.path.append('../../')

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from sql.ETL.load import Load
from sql.ETL.extract import Extract
from sql.ETL.transform import Transform

import pandas as pd

default_args = {
    'owner': 'aalicep.01@gmail.com',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

extract = Extract([
    '../../webscraping/webscraping/spiders/output-action.jsonl',
    '../../webscraping/webscraping/spiders/output-comedy.jsonl',
    '../../webscraping/webscraping/spiders/output-crime.jsonl',
    '../../webscraping/webscraping/spiders/output-drama.jsonl',
    '../../webscraping/webscraping/spiders/output-family.jsonl'
])

transform = Transform(pd.read_json("../../../../../data/raw/output.jsonl", lines=True))

load = Load(pd.read_json("../../../../../data/interim/cleaned.jsonl", lines=True))

with DAG("scrapy_dag", # Dag id
         default_args=default_args,
         start_date=datetime(2021, 1 ,1), # start date, the 1st of January 2021 
         schedule=timedelta(hours=3),  # Cron expression, here it is a preset of Airflow, @daily means once every day.
         catchup=False  # Catchup 
         ) as dag:
    
    scrapy = BashOperator(
        task_id="run_scrapy",
        bash_command="scrapy runspider ../../webscraping/webscraping/spiders/IMDB.py"
        )
    
    join_scrapy_output = PythonOperator(
        task_id='join_scrapy_output',
        python_callable=extract.extract,
        )
    
    save_joined = PythonOperator(
        task_id='save_joined',
        python_callable=extract.save,
        op_kwargs={"output_path": "../../../../../data/raw"},
        )
    
    clean = PythonOperator(
        task_id='clean',
        python_callable=transform.cleaning,
        )
    
    save_cleaned = PythonOperator(
        task_id='save_cleaned',
        python_callable=extract.save,
        op_kwargs={"output_path": "../../../../../data/interim"},
        )
    
    insert_to_postgres = PythonOperator(
        task_id='insert_to_postgres',
        python_callable=load.insert_to_postgres,
        )

scrapy >> join_scrapy_output >> save_joined >> clean >> save_cleaned >> insert_to_postgres


    
    