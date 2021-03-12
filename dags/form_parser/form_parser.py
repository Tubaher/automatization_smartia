import pandas as pd
import logging
from table_parser.table_parser import TableParser

class FormParser(TableParser):
    def __init__(self, metainfo):
        self.metainfo = metainfo

    def __processing_tables(self, full_df):
        """
        This function takes the full dataframe and creates sub dataframes
        per each table define in metainfo

        return: List of dataframes. On data frame per table.
        """
        
        tables_dataframes = {}

        for table_name in self.metainfo["tablas_salida"]:

            # generate a df with specific table sheet
            if self.metainfo[table_name].get("columnas") is not None:
                hoja = self.metainfo[table_name]['hoja']
                table_df = self.__generate_table(full_df["tabla"][hoja], self.metainfo[table_name])
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

        cells_in = [m_c["celda_entrada"] for m_c in meta_record['columnas'] ]
        columns_out = [m_c["nombre_salida"] for m_c in meta_record['columnas'] ]

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
