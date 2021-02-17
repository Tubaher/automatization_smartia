import pandas as pd
import sqlalchemy
from os.path import join
import psycopg2

FILES_DIR = "stuff/tmp"

db_credential = {
    "provider" : "postgresql+psycopg2",
    "user" : "aztozcoembeuas",
    "password" : "37db8b9f5f174d1a58e6f910c9f6114d12bef8320b37d977a5df166d805c5198",
    "host" : "ec2-54-144-251-233.compute-1.amazonaws.com",
    "database" : "dat9k5tq31vohf",
}

def save2db():
    # Loading a .csv  without "" 
    path_file = join(FILES_DIR, "excel_sample.csv")

    df = pd.read_csv(path_file) #,
                    #engine = 'python')
    #df.to_cvs("stuff/tmp/excel_sample_tmp.csv")

    engine = sqlalchemy.create_engine("{}://{}:{}@{}/{}".format(*db_credential.values()))

    print("Saving into database")
    print(df.head())
    # write the DataFrame to a table in the sql database
    df.to_sql("usuarios", engine, if_exists = 'append', index = False)

