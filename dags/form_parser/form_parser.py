import pandas as pd
import logging
from table_parser.table_parser import TableParser

class FormParser(TableParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def generate_dfs(self, path_file):        
        # Process the file according its extension
        full_df = self.file_processing(path_file)

        # Process each table from the columns of the original file
        # return a dataframe per each table
        tables_dataframes = self.__processing_forms_and_tables(full_df)

        return tables_dataframes
        
    def __processing_forms_and_tables(self, full_df):
        """
        This function takes the full dataframe and creates sub dataframes
        per each table define in metainfo

        return: List of dataframes. On data frame per table.
        """
        
        tables_dataframes = {}

        for table_name in self.metainfo["tablas_salida"]:
            
            logging.info("META TABLE: {}".format(self.metainfo[table_name]))
            # generate a df with specific table sheet
            if self.metainfo[table_name].get("columnas") is not None:
                hoja = self.metainfo[table_name]['hoja']
                table_df = self.generate_table(full_df["tabla"][hoja], self.metainfo[table_name]['columnas'])
            # generate a df with specific cells in the full_df
            elif self.metainfo[table_name].get("record") is not None:
                table_df = self.__generate_record(full_df, self.metainfo[table_name])

            logging.info("TABLE DF AFTER LOAD: \n {}".format(table_df))

            tables_dataframes[table_name] = table_df
            
        return tables_dataframes

    @staticmethod
    def alphabet_index(letter):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return alphabet.index(letter)

    def __generate_record(self, full_df, meta_record):

        cells_in = [m_c["celda_entrada"] for m_c in meta_record['record'] ]
        columns_out = [m_c["nombre_salida"] for m_c in meta_record['record'] ]

        # Extract the record values according to the information of cells_in
        record_values = []
        for row, column, sheet_name in cells_in:
            df_row = row - 1
            df_col = self.alphabet_index(column)

            value = full_df["formulario"][sheet_name].loc[df_row, df_col]

            record_values.append(value)

        # rename column names according to the output names
        dict_pandas = {}

        for idx, value in enumerate(record_values):
            dict_pandas[columns_out[idx]] = [value]
        
        return pd.DataFrame(dict_pandas)
