import logging
import pandas as pd

from form_parser.form_parser import FormParser

class ExcelFormParser(FormParser):
    def __init__(self, metainfo):
        super().__init__(metainfo)

    def file_processing(self, path_file):

        full_df = {}
        # 1. numero hoja,
        # 2. numero linea en la que empieza
        # 3. si tiene encabezado o no tiene encabezado

        df_formularios = pd.read_excel(path_file,
                                        header=None,
                                        engine = 'openpyxl',
                                        sheet_name = self.metainfo.get('hojas_formulario'))


        df_tablas = self.__load_table_sheets(path_file)

        full_df['formulario'] = df_formularios
        full_df['tabla'] = df_tablas

        # logging.info("Dict df: {}".format(full_df))
        return full_df

    def __load_table_sheets(self, path_file):
        df_tablas = {}

        if self.metainfo.get('hojas_tabla') is not None:
            for tabla in self.metainfo.get('hojas_tabla'):
                fila = tabla['primera_fila']
                columnas = tabla['columnas_archivo']
                header = tabla['encabezado']
                hoja = tabla['nombre_hoja']
            
                # 1. numero hoja,
                # 2. numero linea en la que empieza
                # 3. si tiene encabezado o no tiene encabezado
                df_table = pd.read_excel(path_file,
                                        header=0 if header else None,
                                        engine= 'openpyxl',
                                        skiprows= fila,
                                        sheet_name = hoja,
                                        usecols = columnas)
                
                df_tablas[hoja] = df_table

        return df_tablas