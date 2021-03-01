import logging
import pandas as pd

from file_parser.file_parser import FileParser

class ExcelParser(FileParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):

        # Get some important variables
        header = self.metainfo['encabezado']
        fila = self.metainfo['primera_fila']
        sep = self.metainfo['separador']

        full_df = pd.read_csv(path_file, 
                            header = 0 if header else None,
                            sep = sep,
                            skiprows = fila)

        return full_df