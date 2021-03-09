from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

#Import the important tasks functions
from tasks.load_form import load_data


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
    'forms_dag',
    default_args=default_args,
    description='ETL dag para formas de clientes',
    # template_searchpath='scripts/msqlserver',
    schedule_interval=None,
)

run_load = PythonOperator(
    task_id='load_form',
    python_callable=load_data,
    dag=dag,
)


run_load 