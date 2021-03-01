import logging
import json
from file_parser.excel_parser import ExcelParser
from file_parser.csv_parser import CSVParser
from file_parser.fijo_parser import FixedWidthParser
import os
from datetime import datetime, date
import sys

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
    elif type_format == "ancho_fijo":
        parser_f = FixedWidthParser(metainfo)
    else:
        logging.error("Type format not defined")

    return parser_f

def get_date_index(files, metainfo):
    dates = []

    type_s = metainfo['modo_lectura']
    date_format = metainfo['formato_fecha']
    separator_file_name = date_format[0]
    separator_date = date_format[3]
    
    for f in files:       
        file_name = os.path.splitext(f)[0]
        logging.info("file_name {}".format(file_name))
        date_string = separator_date.join(file_name.split(separator_file_name)[1::])
        logging.info("Date_string {}".format(date_string))
        parsed_date = datetime.strptime(date_string, date_format)
        dates.append(parsed_date)

    if type_s == "ultimo":
        index = dates.index(max(dates))
    elif type_s == "hoy":
        dt = datetime.combine(date.today(), datetime.min.time())
        try:
            index = dates.index(dt)
        except:
            logging.error("Error there are not files with the today date")
            sys.exit(1)
    
    logging.info("Index of file {}".format(index))

    return index

def load_files_names(metainfo):
    files = os.listdir(metainfo["ruta_archivos"])
    files.remove('processed')
    
    if metainfo['modo_lectura'] =='ultimo':
        files = [files[get_date_index(files, metainfo)]]
    elif metainfo['modo_lectura'] =='hoy':
        files = [files[get_date_index(files, metainfo)]]

    return files

def validate_metainfo(metainfo):
    #TODO: print errors when some attributes are missing in the metainfo.json
    # accoding to each type, because each type has different attributes

    #also validate if the fields of the output table are correct, check if the names
    #are correct according to the variable TABLES_FIELDS in config
    print("VALIDATE HERE")