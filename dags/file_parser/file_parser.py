import pandas as pd
import logging

class FileParser:
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
            filter_columns_names_out = []
            filter_columns_names_in = []

            meta_columns_with_operations = []
            
            for meta_column in self.metainfo[table_name]:        
                # filter the meta columns with operations
                if meta_column.get("operaciones") is not None:
                    meta_columns_with_operations.append(meta_column)
                else:
                    # filter the columns that does not have operations
                    filter_columns_names_in.append(meta_column["nombre_entradas"][0])
                    filter_columns_names_out.append(meta_column["nombre_salida"])


            # generate a df with the filter the columns
            table_df = full_df[filter_columns_names_in]

            # rename column names according to the output names
            dict_names = { past_name: new_name for past_name, new_name in zip(filter_columns_names_in,filter_columns_names_out)}
            table_df = table_df.rename(columns = dict_names)

            logging.info("TABLE DF AFTER OPERATIONS : \n {} \n {}".format(table_df, table_df.dtypes))

            # perform operation between columns, 
            # adding new columns to the right of the table_df
            self.__operation_columns(table_df, full_df, meta_columns_with_operations)

            logging.info("TABLE DF BEFORE OPERATIONS: \n {}".format(table_df))

            tables_dataframes[table_name] = table_df
            
        return tables_dataframes
    

    def __operation_columns(self, table_df, full_df, meta_columns_with_operations):
        """
        This function performs the operations between columns, and stores the results
        in a new column.
        """
        
        for m_column in meta_columns_with_operations:

            str_exec = "table_df[\"{}\"] = ".format(m_column["nombre_salida"])

            inter_layer = m_column["nombre_entradas"] + m_column["operaciones"]
            inter_layer[::2] = m_column["nombre_entradas"]
            inter_layer[1::2] = m_column["operaciones"]

            for idx, value in enumerate(inter_layer):
                if idx % 2 == 0:
                    str_exec += "full_df[{}]".format(value) + " "
                else:
                    str_exec += str(value) + " "
                    
            
            logging.info("STR EXEC: {}".format(str_exec))
            exec(str_exec)

            # ANOTHER way to process the operations between columns
            # OPERATIONS = {
            #     "+" : lambda a, b: a + b,
            #     "-" : lambda a, b: a - b
            # }
            
            # auxiliar_operator = table_df[ m_column["nombre_entradas"][0] ]

            # for idx, op in enumerate(m_column["operaciones"]):
            #     column1 = auxiliar_operator
            #     column2 = table_df[ m_column["nombre_entradas"][idx + 1] ]
            #     auxiliar_operator = OPERATIONS[op](column1, column2)
            
            # table_df[m_column["nombre_salida"]] = auxiliar_operator