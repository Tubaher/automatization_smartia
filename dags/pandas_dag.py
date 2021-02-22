from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os

from load_data import load_excel
from save_db import save2db

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

def just_a_function():
    print("It's runnig this section of code")
    print(" Parten dir: ", os.getcwd())

run_load = PythonOperator(
    task_id='pandas_load',
    python_callable=load_excel,
    dag=dag,
)

run_save = PythonOperator(
    task_id='pandas_sql',
    python_callable=save2db,
    dag=dag,
)

run_load >> run_save