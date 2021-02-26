import pandas as pd
import sqlalchemy as sa
from os.path import join
import psycopg2
import config
import pyodbc
import utils 
import os 
import logging

def save2db(**kwargs):

    # Loading metainfo
    metainfo = utils.load_metainfo(kwargs)

    if metainfo is not None:

        # Load the engine of our database
        # engine = sa.create_engine("{}://{}:{}@{}/{}".format(*config.db_credential.values()))
        engine = sa.create_engine("{}://{}:{}@{}:{}/{}?driver={}".format(*config.db_credential_sqlserver.values()))
    
        # Loading the tmp .csv from dir
        dir_tmp_files = join( config.TMP_FILES_DIR, metainfo["cliente"])

        for f in os.listdir(dir_tmp_files) :
            filename, filename_ext = os.path.splitext(f)

            table_name, _ = filename.split("_")

            if filename_ext == ".csv":
                path_file = join(dir_tmp_files, f)

                # Read the csv
                df = pd.read_csv(path_file)

                # Saved the result in the database
                logging.info("Saving {} into table {}".format(f, table_name))
                try:
                    df.to_sql(table_name, engine, if_exists = 'append', index = False)
                except Exception as e:
                    logging.warning("The file {} could not be saved into table {}".format(f, table_name))
                else:
                    #if not error occurs remove the temporal file
                    os.remove(path_file)

            else:
                logging.warning("The file {} extension is not .csv".format(f))