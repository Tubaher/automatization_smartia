import logging
import json
from file_parser.excel_parser import ExcelParser
from file_parser.csv_parser import CSVParser
import os
from datetime import datetime, date

def load_metainfo(kwargs):

    metainfo = None

    # Loading config file when you execute the task
    if kwargs['params'].get('cfg_file') is not None:
        logging.info("Loading meta information {}".format(kwargs['params']['cfg_file']))

        cfg_file_dir = kwargs['params']['cfg_file']

        with open(cfg_file_dir) as f:
            metainfo = json.load(f)

        logging.info("Metainfo {}".format(metainfo))
    
    # loading when you execute the full dag
    elif kwargs['dag_run'] is not None:
        if kwargs['dag_run'].conf.get['cfg_file'] is not None:
            logging.info("Loading meta information {}".format(kwargs['dag_run'].conf['cfg_file']))

            cfg_file_dir = kwargs['dag_run'].conf['cfg_file']

            with open(cfg_file_dir) as f:
                metainfo = json.load(f)

            logging.info("Metainfo {}".format(metainfo))
    else:
        logging.error('No metainfo.json. You need to provide metainfo.json')
    
    
    return metainfo

def WrapperFileParser(metainfo):
    """ This function returns a parser type according to the type defined in metainfo

        return: a FileParser given the type in metainfo
    """
    type_format = metainfo["tipo"].translate({".":""})

    parser_f = None

    if type_format == "xlsx":
        parser_f = ExcelParser(metainfo)
    elif type_format == "csv":
        parser_f = CSVParser(metainfo)
    else:
        logging.error("Type format not defined")

    return parser_f

def get_date_index(files, type_s = "ultimo"):
    dates = []
    for f in files:
        file_name = os.path.splitext(f)[0]
        date_string = '/'.join(file_name.split("_")[1::])
        parsed_date = datetime.strptime(date_string, "%Y/%m/%d")
        dates.append(parsed_date)
    
    if type_s == "ultimo":
        index = dates.index(max(dates))
    elif type_s == "hoy":
        index = dates.index(date.today())
    
    return index

def load_files_names(metainfo):
    files = os.listdir(metainfo["ruta_archivos"])
    
    if metainfo['modo_lectura'] =='ultimo':
        files = files[get_date_index(files, "ultimo")]
    elif metainfo['modo_lectura'] =='hoy':
        files = files[get_date_index(files, "hoy")] 

    return files