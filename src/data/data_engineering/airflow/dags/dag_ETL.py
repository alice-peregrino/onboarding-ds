from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("dag_ETL", # Dag id
         start_date=datetime(2021, 1 ,1), # start date, the 1st of January 2021 
         schedule_interval='',  # Cron expression, here it is a preset of Airflow, @daily means once every day.
         catchup=False  # Catchup 
         ) as dag:
    
    scrapy = BashOperator(
        task_id="run_scrapy",
        bash_command=""
        )