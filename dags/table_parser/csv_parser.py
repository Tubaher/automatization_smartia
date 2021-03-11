import logging
import pandas as pd
from utils import pandas_utils
from file_parser.file_parser import TableParser

class CSVParser(TableParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):

        # TODO: Put an option when the csv is corrupted with extras doble semicolons
        # Check how to deal with float number, differentiate . and ,

        # Get some important variables
        header = self.metainfo['encabezado']
        fila = self.metainfo['primera_fila']
        sep = self.metainfo.get('separador')

        full_df = pd.read_csv(path_file, 
                            header = 0 if header else None,
                            sep = sep if sep is not None else ",",
                            skiprows = fila)

        logging.info("FULL_DF: \n {}".format(full_df))

        # If converters are setting, you can use them to operate over columns
        # and correct some pior problem with the columns
        # With this converter, we deal with csv corrupted information
        # e.g: multiple quotation marks, float number separator, and so on
        
        if self.metainfo.get('converters') is not None:
            full_df = pandas_utils.clean_corruptions(full_df, self.metainfo['converters'])


        # Remove beginning and ending spaces
        # full_df = pandas_utils.custom_strip(full_df)

        return full_df