import datetime

import pytest
# from dags.tables_dag import dag
from airflow import DAG

@pytest.fixture
def test_dag():
    return DAG(
        'test_dag',
        default_args={'owner': 'airflow', 'start_date': datetime.datetime(2018, 1, 1)},
        schedule_interval=None,
    )

pytest_plugins = ["helpers_namespace"]

@pytest.helpers.register
def run_task(task, dag):
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
        end_date=dag.default_args["start_date"],
    )

