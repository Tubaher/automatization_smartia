import pandas as pd
import json
import os
import config
import logging
from os.path import join
from glob import glob
from file_parser.file_parser import FileParser
import utils 
from datetime import datetime

def load_data(**kwargs):

    # Loading metainfo
    metainfo = utils.load_metainfo(kwargs)

    if metainfo is not None:

        # Define a parser to the current files format
        fileParser = utils.WrapperFileParser(metainfo)

        # Loading file with a especific format
        file_path = join(metainfo["ruta_archivos"],"processed")
        files = os.listdir(metainfo["ruta_archivos"])

        #Create the processed file if not exists
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        for f in files:
            filename, filename_ext = os.path.splitext(f)

            #check the extension file
            if filename_ext == "."+metainfo["tipo"].translate({".":""}):
                path_file = join(metainfo["ruta_archivos"], f)
                
                # Parser to df frame
                logging.info("PATH FILE: {} ".format(path_file))

                dataframes = fileParser.generate_dfs(path_file)

                #Saving the data frames in temporals .csv
                for table_name, df in dataframes.items():
                    folder_name = metainfo["cliente"]
                    tmp_folder_dir = join(config.TMP_FILES_DIR, folder_name)
                    if not os.path.exists(tmp_folder_dir):
                        os.mkdir(tmp_folder_dir)

                    # Name of the temporal file .csv
                    output_file_name = table_name + "_"+ datetime.now().strftime('%d-%m-%Y-%H-%M') + ".csv"
                    
                    tmp_file_dir = join(tmp_folder_dir, output_file_name)

                    df.to_csv( tmp_file_dir , index = False)
            elif (filename == "processed"):
                continue
            else:
                logging.warning("The extension does not match with files")