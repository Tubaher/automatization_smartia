# Using DAGs for ETL development with Pandas
First we recommend to use a venv. In Linux it is done by:

```bash
    python3 -m venv /path/to/new/virtual/environment
```
Then, we should start it by:
```bash
    source /path/to/new/virtual/environment/bin/activate
```
Here we have to make sure to downgrade or upgrade to the specific pip version:
```bash
    pip install --upgrade pip==20.2.4
```
After this, we just have to follow the steps in [Airflow Documentation Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html). 

After, we have the airflow webserver and airflow scheduler running in different terminals we can test our DAGs