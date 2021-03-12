from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os
# from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

#Import the important tasks functions
from tasks.load_table import load_data
from tasks.pandas_sql import save2db

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
    'tables_dag',
    default_args=default_args,
    description='ETL dag to process data files with different extensions',
    #template_searchpath='scripts/msqlserver',
    schedule_interval=None,
)

run_load = PythonOperator(
    task_id='load_table',
    python_callable=load_data,
    dag=dag,
)

run_save = PythonOperator(
    task_id='pandas_sql',
    python_callable=save2db,
    dag=dag,
)

# opr_call_sproc = MsSqlOperator(
#     task_id='call_sproc',
#     mssql_conn_id='mssql_smartia',
#     sql='call-sproc1.sql',
#     dag=dag,
# )

run_load >> run_save #>> opr_call_sproc