from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os

#Import the important tasks functions
from tasks.load_data import load_data
from tasks.save_db import save2db

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0,0,0,0,0),
    'email': ['tubarao0705@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'pandas_dag',
    default_args=default_args,
    description='ETL dag to process data files with different extensions',
    schedule_interval=None,
)

run_load = PythonOperator(
    task_id='pandas_load',
    python_callable=load_data,
    dag=dag,
)

run_save = PythonOperator(
    task_id='pandas_sql',
    python_callable=save2db,
    dag=dag,
)

run_load >> run_save