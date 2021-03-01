import logging
import pandas as pd

from file_parser.file_parser import FileParser

class ExcelParser(FileParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):

        # First load the information from columns
        info_columns = self.metainfo['info_columnas']

        if info_columns["read_from"] == "external_file":
            # Load the column info from an external file xlsx
            column_names, intervals = self.__columns_info_from_extfile(info_columns)

        elif info_columns["read_from"] == "metainfo_file":
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

        return full_df

    def __columns_info_from_extfile(self, info_columns):
        columns_dfs = pd.read_excel(filepath= info_columns['dir'],
                        header= None,
                        skiprows= info_columns['primera_fila'],
                        sheet_name = info_columns['hoja'],
                        usecols = info_columns['loc_nombres_campo'] + "," + info_columns['loc_intervalos'])

        logging.info("COLUMNS INFO: \n {}".format(columns_dfs))

        columns_names = list(columns_dfs[0])
        intervals = [(v1,v2) for (v1,v2) in zip(columns_dfs[1],columns_dfs[2])]
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
        init_index = info_columns['indice_inicial']
        intervals = self.__parser_intervals(intervals, 
                                            info_columns['estilo_intervalos'],
                                            info_columns['indice_inicial'])

        return columns_names, intervals

    def __parser_intervals(self, intervals , estilo, init_index = 0):
        """ The interval always must be of style close-open.
            So, we have to transform to this style from any received style
        """

        if estilo == "close_close":
            intervals = [ (v1 - init_index, v2 - init_index + 1) for (v1, v2) in intervals]
        elif estilo == "close_open" :
            intervals = [ (v1 - init_index, v2 - init_index) for (v1, v2) in intervals]
        # elif estilo == "open_close" :
        #     intervals = [ (v1 - init_index + 1, v2 - init_index + 1) for (v1, v2) in intervals]
        # elif estilo == "open_open" :
        #     intervals = [ (v1 - init_index + 1, v2 - init_index) for (v1, v2) in intervals]

        return intervals