import pandas as pd
import logging

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

            # generate a df with specific cells in the full_df
            table_df = self.__generate_columns(full_df, self.metainfo[table_name])

            logging.info("TABLE DF AFTER LOAD: \n {}".format(table_df))

            tables_dataframes[table_name] = table_df
            
        return tables_dataframes

    @staticmethod
    def alphabet_index(letter):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return alphabet.index(letter)

    def __generate_columns(self, full_df, columns):

        #extract the names in and out from meta columns
        logging.info('Columnas: {}'.format(columns))

        if columns['modo'] == 'formulario':
            hoja = columns['hoja']
            columns_in = [m_c["nombre_entrada"] for m_c in columns['columnas'] ]
            columns_out = [m_c["nombre_salida"] for m_c in columns['columnas'] ]

            # process columns_in to get the right cell
            logging.info('Columnas de entrada: {}'.format(columns_in))

            cells = [ (row-1, self.alphabet_index(column)) for row, column in columns_in]
            logging.info('cells value: {}'.format(cells))
            #filter some colums from the full_df
            # logging.info('Full dataframe: {}'.format(full_df))
            logging.info('values: {}'.format(full_df['formulario']['Creacion Campaña SMS']))
            columns_value = [full_df[columns['modo']][hoja].loc[cell[0], cell[1]] for cell in cells]
            logging.info('Columns value: {}'.format(columns_value))
            # rename column names according to the output names
            dict_pandas = {}

            for idx, value in enumerate(columns_value):
                dict_pandas[columns_out[idx]] = [value]
            
            table_df = pd.DataFrame(dict_pandas)

        elif columns['modo'] == 'tabla':
            hoja = columns['hoja']
            #extract the names in and out from meta columns
            columns_in = [m_c["nombre_entrada"] for m_c in columns['columnas'] ]
            columns_out = [m_c["nombre_salida"] for m_c in columns['columnas'] ]

            #filter some colums from the full_df
            table_df = full_df[columns['modo']][hoja][columns_in]

            # rename column names according to the output names
            dict_names = { past_name: new_name for past_name, new_name in zip(columns_in,columns_out)}
            table_df = table_df.rename(columns = dict_names)


        return table_df
