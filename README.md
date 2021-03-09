# Airflow ETL with Pandas Control

This repository comprises an Extract, Transform, Load (ETL) system to deal with two kind of files: tables and forms. For each type, we developed a DAG to extract the information, transform and finally load into the database. These DAG are stored in [dags/tables_dag.py](dags/tables_dag.py) and [dags/forms_dag](dags/forms_dag). 

A dag must be executed joining with a metainfo configuration file. This file help us to define how 
to treat the input data, what are the output table within the database, among other things. This metafiles and how to configure them can be found in [metainfo/](metainfo/)

To run this repository, we recommend to read the [metainfo](metainfo/) files and follow the next steps:

1. Installation
2. Connection to Microsof SQL Server
3. Sample Execution

To update this repository, we recommend to change just few things in the repository according your needs that are:

1. Parser
2. Converters

## Installation
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
Next, we can install the requirements
```bash
    pip install -r requirements.txt
```
After this, we just have to follow the steps in [Airflow Documentation Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html). 

After, we have the airflow webserver and airflow scheduler running in different terminals we can test our DAGs


## Connection to Microsoft SQL Server
The first thing we should download is the SQL Server. We can choose from the [Development version or the Express version](https://www.microsoft.com/es-es/sql-server/sql-server-downloads).

After that we should install it and then we can procede to install the [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) to have a GUI where we can manage our SQL Server. Of course, we can just use the command line.

Once, we have all the components of MSQL Server installed, we can start to create a test database, and a table where we want to write new registers from Pandas. Now, we should stablish a comunication from the SQL Server to our WSL enviroment. then, we need to follow these steps:

1. We have to enable the TCP/IP connections of the SQL Server
To do this task, we start by pressing **Windows + R** and in the Run Windows we type **	SQLServerManager15.msc** to open the SQL server configuration Manager. **Note**The command is valid fort SQL Server 2019 version, you can check the right command for your version [here](https://www.sqlshack.com/how-to-use-sql-server-configuration-manager/#:~:text=The%20SQL%20Server%20configuration%20manager,msc%E2%80%9D%20file.)

2. Inside the SQL Server Manager, we go to the SQL Server network configuration and select the protocl for MSSQLSERVER and enable the TCP/IP option by right clicking in the item. 
![SQL Manager](assets/sql_manager.PNG)

3. After that, we go to the SQL Server Services and restart the SQL Server running so the changes are applied.
![SQL restart](assets/restart.PNG)

4. Then, we should allow this port in the Windows firewall using an Inbound rule in the port we select for TCP:
![TCP firewall 1](assets/tcp_1.PNG)
![TCP firewall 1](assets/tcp_2.PNG)

Now we have to connect from WSL2 to the SQL Server to use Airflow and the tasks we have created. Then, the first thing we need is to install the ODBC driver for our distribution of linux in WSL. Here is the web page for the different versions of [MSQL ODBC for linux](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#ubuntu17). In this case, we have use Ubuntu in WSL2, then we are using the same version for the installation of the ODBC. In the link above there is a bash script for Ubuntu distribution wich install the ODBC and place it by default into **/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.1.1**. 

## Sample Execution

### Testing a task

To test a task separately, we can use the bash files [execute_task_forms.sh](execute_task_forms.sh) or [execute_task_tables.sh](execute_task_tables.sh) in the following way:

```
    bash execute_task_tables.sh <task_name> <metainfo_file.json>
```

### Executing the complete dag

To execute the complete dag, we can use the bash file [execute_dag.sh](execute_dag.sh) in the following way:

```
    bash execute_dag <dag_name> <dag_id_int> <metainfo_file.json>
```

## Parser

We create two parent classes ([table_parser.py](dags/table_parser/table_parser.py) and [forms_parser.py](dags/form_parser/form_parsers.py)) to transform the received files into a data frames of pandas. In this way, to parser an specific file extension into a dataframe, we just need to inherit the corresponding parent class and update the `file_processing(self, path_file)` function according our needs. You can follow the template of one the existing classes in [table_parser/](dags/table_parser/) or [form_parser/](dags/form_parser/).

After creating the new class, you need to call it in [utils.py](dags/utils/utils.py) and define it within the function `WrapperFileParser(metainfo)` according its type.


## Converters

In some cases, the input files could content corrupted information, such as: extra doble quotation marks, blank spaces, incorrect float number separator, among others. For this reason, we create a way to deal with these problems, called `converters`. The converters are special functions that are executed per column to correct the imperfections in data. Currently, we developed four functions which can be configurated in the `metainfo_file.json`. The definition of each function can be found in [config.py](dags/utils/config.py) within the variable:

```
CONVERTER_OPERATIONS = {
    "remove"    : lambda val, record: record.replace(val,''),
    "replace"   : lambda val1, val2, record: record.replace(val1,val2),
    "float_sep" : lambda val, record: float(record.replace(val, '.')),
    "strip"     : lambda record : record.strip()
}
```

If you have to deal with an specific data corruption per column, you just need to configure a new function within this dictionary.