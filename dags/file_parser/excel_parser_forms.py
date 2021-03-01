import logging
import pandas as pd

from file_parser.file_parser import FileParser

class ExcelParser(FileParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):
        # TODO: cargar respecto a
        hoja = self.metainfo['hoja']


        # 1. numero hoja,
        # 2. numero linea en la que empieza
        # 3. si tiene encabezado o no tiene encabezado
        full_df = pd.read_excel(path_file,
                                header=None,
                                sheet_name = hoja)

        # names = config.column_names) #engine = 'python')

        return full_df
