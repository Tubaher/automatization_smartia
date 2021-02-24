import logging
import json
from file_parser.excel_parser import ExcelParser
from file_parser.csv_parser import CSVParser

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