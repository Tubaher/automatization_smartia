# Setting Up Metainfo Files

In short, the metainfo files help us to set up the following information:

* The format, directory, type and extension of the input files
* How to deal with the input data (converters)
* The structure and information of the output data, which will be stored in the database.

In the following, we detail the information that must contain the metainfo files. We have to keep in mind that there are metainfo files for `tables` and `forms`. Also, there are general attributes, which have all the metainfo files, and other attributes that are setting up according to the type.

## General Attributes

The general attributes of all the metainfo files are the following:

| Attribute      | Description                           | Options                                                                                                                                                                              |
|----------------|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tipo           | Parser Type to apply                  | csv, xlsx, ancho_fijo, xlsx_form                                                                                                                                                     |
| file_extension | Extension of input files              | csv, xlsx, txt, raw, etc                                                                                                                                                             |
| ruta_archivos  | Directory to the input files          | stuff/input_files                                                                                                                                                                    |
| modo_lectura   | Read mode to process the input files. | all_dir: process all the files in the 'ruta_archivos' dir<br>ultimo:  process the last file in the 'ruta_archivos' dir<br>hoy:     process the today file in the 'ruta_archivos' dir |
| formato_fecha  | Define the date format of input files | e.g: _%Y_%m_%d                                                                                                                                                                       |
| client         | Client name of the input file         | e.g: BANCO_AGRICOLA                                                                                                                                                                  |

```json
    {
    "tipo": "csv",
    "file_extension" : "csv",
    "ruta_archivos": "stuff/input_files/CSV_EXAMPLES_SIMPLE",
    "modo_lectura": "all_dir",
    "formato_fecha" : "_%Y_%m_%d",
    "cliente": "CSV_EXAMPLES_SIMPLE",
    "primera_fila": 0,
    "encabezado": false,
    "separator": ",",

    "tablas_salida" : ["usuarios"] 
    }
```