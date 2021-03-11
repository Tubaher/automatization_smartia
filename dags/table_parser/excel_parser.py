import logging
import pandas as pd
from utils import pandas_utils

from file_parser.file_parser import TableParser

class ExcelParser(TableParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):
        # TODO: cargar respecto a
        hoja = self.metainfo['hoja']
        fila = self.metainfo['primera_fila']
        columnas = self.metainfo['columnas']
        header = self.metainfo['encabezado']

        # 1. numero hoja,
        # 2. numero linea en la que empieza
        # 3. si tiene encabezado o no tiene encabezado
        full_df = pd.read_excel(path_file,
                                header=0 if header else None,
                                skiprows= fila,
                                sheet_name = hoja,
                                usecols = columnas)

        # names = config.column_names) #engine = 'python')

        # If converters are setting, you can use them to operate over columns
        # and correct some pior problem with the columns
        # With this converter, we deal with csv corrupted information
        # e.g: multiple quotation marks, float number separator, and so on
        
        if self.metainfo.get('converters') is not None:
            full_df = pandas_utils.clean_corruptions(full_df, self.metainfo['converters'])


        return full_df
