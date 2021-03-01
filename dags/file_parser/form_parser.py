import pandas as pd
import logging
import config

class FormParser:
    def __init__(self, metainfo):
        self.metainfo = metainfo

    def generate_dfs(self, path_file):        
        # Process the file according its extension
        full_df = self.file_processing(path_file)

        # Process each table from the columns of the original file
        # return a dataframe per each table
        tables_dataframes = self.__processing_tables(full_df)

        return tables_dataframes

    # def file_processing(self, path_file):
    #     #TODO: require a function to load the file into a data frame
    #     df = pd.DataFrame(path_file)

    #     return df

    def __processing_tables(self, full_df):
        """
        This function takes the full dataframe and creates sub dataframes
        per each table define in metainfo

        return: List of dataframes. On data frame per table.
        """
        
        tables_dataframes = {}

        for table_name in self.metainfo["tablas_salida"]:

            columns = []
                  
            for meta_column in self.metainfo[table_name]:
                columns.append(meta_column)

            # generate a df with specific cells in the full_df
            table_df = self.__generate_columns(full_df, columns)

            logging.info("TABLE DF AFTER LOAD: \n {}".format(table_df))

            tables_dataframes[table_name] = table_df
            
        return tables_dataframes

    @staticmethod
    def alphabet_index(letter):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return alphabet.index(letter)

    def __generate_columns(self, full_df, columns):

        #extract the names in and out from meta columns
        columns_in = [m_c["nombre_entradas"][0] for m_c in columns ]
        columns_out = [m_c["nombre_salida"] for m_c in columns ]

        # process columns_in to get the right cell
        cells = [ (row-1, self.alphabet_index(column)) for row, column in columns_in]
        
        #filter some colums from the full_df
        columns_value = [full_df.loc[cell[0], cell[1]] for cell in cells]

        # rename column names according to the output names
        dict_pandas = {}

        for idx, value in columns_value:
            dict_pandas[columns_out[idx]] = [value]
        
        table_df = pd.DataFrame(dict_pandas)

        return table_df
