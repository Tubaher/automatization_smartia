FROM apache/airflow:2.0.1
USER root
RUN apt-get update \
  && apt-get install -y build-essential\
  && apt-get install -y unixodbc unixodbc-dev\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir --user apache-airflow-providers-microsoft-mssql[odbc] \
  && pip install --no-cache-dir --user openpyxl
