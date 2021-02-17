from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

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
    description='DAG for formatting a csv',
    schedule_interval=None,
)

def just_a_function():
    print("It's runnig this section of code")

run_etl = PythonOperator(
    task_id='pandas_load',
    python_callable=just_a_function,
    dag=dag,
)

run_etl