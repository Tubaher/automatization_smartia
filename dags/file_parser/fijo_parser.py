import logging
import pandas as pd
from utils import pandas_utils
import re

from file_parser.file_parser import FileParser

class FixedWidthParser(FileParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):

        # First load the information from columns
        info_columns = self.metainfo['info_columnas']

        if info_columns.get("read_from") == "external_file":
            # Load the column info from an external file xlsx
            column_names, intervals = self.__columns_info_from_extfile(info_columns)
        
        elif info_columns.get("read_from") == "metainfo_file":
            # Load the column info from the metainfo file directly
            column_names, intervals = self.__columns_info_from_metainfo(info_columns)

        # Get some important variables
        header = self.metainfo['encabezado']
        fila = self.metainfo['primera_fila']
        sep = self.metainfo['separador']

        full_df = pd.read_fwf(path_file, 
                            colspecs = intervals, 
                            header = 0 if header else None,
                            names = column_names, 
                            sep = sep,
                            skiprows = fila)

        logging.info("FULL_DF: \n {}".format(full_df))

        # If converters are setting, you can use them to operate over columns
        # and correct some pior problem with the columns
        # With this converter, we deal with csv corrupted information
        # e.g: multiple quotation marks, float number separator, and so on

        if self.metainfo.get('converters') is not None:
            full_df = pandas_utils.clean_corruptions(full_df, self.metainfo['converters'])


        return full_df

    def __columns_info_from_extfile(self, info_columns):
        columns_dfs = pd.read_excel(info_columns['dir'],
                        header= None,
                        skiprows= info_columns['primera_fila'] - 1,
                        sheet_name = info_columns['hoja'],
                        usecols = info_columns['loc_nombres_campo'] + "," + info_columns['loc_intervalos'])

        #rename columns names
        columns_dfs.columns = [ i for i in range(len(columns_dfs.columns))]

        logging.info("COLUMNS INFO: \n {}".format(columns_dfs))

        columns_names = list(columns_dfs[0])

        # we expect to receive two or three columns and perform different process
        # to separate the intervals
        if len(columns_dfs.columns) == 2:
            intervals = [self.__sep_intervals(str_val) for str_val in columns_dfs[1]]
        elif len(columns_names.columns) == 3:
            intervals = [(int(v1),int(v2)) for (v1,v2) in zip(columns_dfs[1],columns_dfs[2])]

        logging.info("INTERVALS: {}".format(intervals))

        intervals = self.__parser_intervals(intervals, 
                                            info_columns['estilo_intervalos'],
                                            info_columns['indice_inicial'])
        
        logging.info("COLUMNS NAMES: {}".format(columns_names))
        logging.info("INTERVALS: {}".format(intervals))
        return columns_names, intervals

    def __columns_info_from_metainfo(self, info_columns):
        # TODO: load information about columns directly from the metainfo .json
        
        columns_names = [ c["nombre_columna"] for c in info_columns["columnas"]]

        intervals = [ tuple(c.get("intervalo")) for c in info_columns["columnas"]]

        # If we use ancho instead of intervalo
        if len(intervals) == 0:
            intervals = []
            acu = 0
            for c in info_columns["columnas"]:
                val1 = acu
                val2 = acu + c["ancho"] + 1
                intervals.append((val1,val2))
                acu += val2
            info_columns['estilo_intervalos'] = "close-open"
            
        #move intervals according to the initial inde
        intervals = self.__parser_intervals(intervals, 
                                            info_columns['estilo_intervalos'],
                                            info_columns['indice_inicial'])

        logging.info("INTERVALS: {}".format(intervals))

        return columns_names, intervals

    def __parser_intervals(self, intervals , estilo, init_index = 0):
        """ The interval always must be of style close-open.
            So, we have to transform to this style from any received style
        """

        if estilo == "close-close":
            intervals = [ (v1 - init_index, v2 - init_index + 1) for (v1, v2) in intervals]
        elif estilo == "close-open" :
            intervals = [ (v1 - init_index, v2 - init_index) for (v1, v2) in intervals]
        # elif estilo == "open_close" :
        #     intervals = [ (v1 - init_index + 1, v2 - init_index + 1) for (v1, v2) in intervals]
        # elif estilo == "open_open" :
        #     intervals = [ (v1 - init_index + 1, v2 - init_index) for (v1, v2) in intervals]

        return intervals

    def __sep_intervals(self, str_val):
        interval = re.findall(r'\b\d+\b', str(str_val))
        
        return (int(interval[0]), int(interval[1]))