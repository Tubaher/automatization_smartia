import pandas as pd
from os.path import join

FILES_DIR = "stuff/input_files/examples"


FIELD_NAMES = ["id", "nombres", "apellidos", "genero", "condicion", 
                    "equipo", "cedula", "trabajo", "lugar" ]

def load_excel():
    # Loading a .csv  without "" 
    path_file = join(FILES_DIR, "excel_sample.xlsx")

    df = pd.read_excel(path_file, 
                    header = None,
                    names = FIELD_NAMES) #,
                    #engine = 'python')

    df.to_csv("stuff/tmp/excel_sample.csv", index = False)

    print(df.head())