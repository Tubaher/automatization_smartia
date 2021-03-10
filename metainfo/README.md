- [Setting Up Metainfo Files](#setting-up-metainfo-files)
  - [General Attributes](#general-attributes)
    - [Metacolumns](#metacolumns)
    - [Converters](#converters)
  - [Table Files - Metainfo Style](#table-files---metainfo-style)
    - [CSV Files Attributes](#csv-files-attributes)
    - [Excel or xlsx Files Attributes](#excel-or-xlsx-files-attributes)
    - [Fixed Width or "ancho_fijo" Files Attributes](#fixed-width-or-ancho_fijo-files-attributes)
      - [**Loading from an external .xlsx file**](#loading-from-an-external-xlsx-file)
      - [**Loading within the same metainfo file**](#loading-within-the-same-metainfo-file)
  - [Form Files - Metainfo Style](#form-files---metainfo-style)
    - [Excel Form or xlsx Form Files Attributes](#excel-form-or-xlsx-form-files-attributes)

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
| encabezado    | true or false if the file contains header or not.                                                                                           | true, false                 |
| primera fila  | The first row from where the records are read.<br>If the file contains a header this attribute is <br>the row where the header is presented | 0 (default)            |
| tablas_salida | Specify the name of output tables, which will be <br>stored in database                                                                     | e.g: ["usuarios", "gastos"] |

### Metacolumns
Here, for each table name you can define an attribute that contains a list of metacolumns. These metacolumns indicate the values ​​contained in each output column. Also, we can configure some operation between input columns and default values per column.

Then, we draw out an example of this attribute with four columns:

1. Take an input column and move directly to an output column
2. Set an output column with an default value
3. Perform an operation with two input columns and store the result in an output column.
4. Perform an operation with an input column and store the result in an output column.
 
```json
    "usuarios" : [
        {
            "nombre_salida": "id",
            "nombre_entradas": [0]
        },
        {
            "nombre_salida": "nombres",
            "default": "Pepito"
        },
        {
            "nombre_salida": "apellidos",
            "nombre_entradas": [1, 2],
            "operaciones" : ["+"]
        },
        {
            "nombre_salida": "gastos",
            "nombre_entradas": [3],
            "operaciones" : ["\100"]
        },

    ]
```

### Converters

Converters are optional tools focus to deal with corruptions in input files. A converter is a simple function that is executed over a complete column and changes something in all the records. For example, if a column contains double quotation marks at the beginning and end of each record, we can use a remove function to erase that corruption.

Currently, we implement four basic converter functions that are:

| Function           | Description                                                                 | Optional Values            |
|--------------------|-----------------------------------------------------------------------------|----------------------------|
| remove(val)        | Remove the val in each record per column                                    | e.g. ["\"", "4", "-"]      |
| replace(val1,val2) | Replace the val1 by val2 in each record per column                          | e.g. [["-","_"], [".",","] |
| float_sep(val1)    | Define the float sep in the input file in each record per column            | e.g. [","]                 |
| strip()            | Removes the blank spaces at the beginning and end in each record per column |                            |

The definition of each function can be found in [config.py](../dags/utils/config.py) in the dictionary `CONVERTER_OPERATIONS`

Then, we have a little example of some converters in the metainfo.json file.

```json
    "converters" : [
        {
            "columnas_entrada" : "all",
            "operation" : "remove",
            "values" : ["\""]
        },
        {
            "columnas_entrada" : [5, 6],
            "operation" : "float_sep",
            "values" : [","]
        }
    ],
```

The first converter removes doble quotation marks over all the input columns. The second converter changes the float number separator "," to the correct accepted representation.

For a further exploration, you can review [metainfo_csv_alterado_sample.json](metainfo_csv_alterado_sample.json)

## Table Files - Metainfo Style
### CSV Files Attributes

The common setting attributes for .csv files are

| Attribute     | Description                                                                                                                                 | Options                     |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| separator     | Specify the column separator in a csv file                                                                                                  | "," (default), ";"," "      |

### Excel or xlsx Files Attributes

The common setting attributes for .xlsx files are:

| Attribute | Description                                     | Options       |
|-----------|-------------------------------------------------|---------------|
| hoja      | Sheet name of the input files                   | e.g: "Hoja 1" |
| columnas  | Columns to take into account in the input files | e.g: "A:I"    |

### Fixed Width or "ancho_fijo" Files Attributes

In this kind of file, we have to specified the width per each column. To do that, we elaborate two ways to read this information: through an external file or through the same metainfo file.

#### **Loading from an external .xlsx file**

To set the file where we want to extract the information per column, we have to configure an attribute `info_columnas` in the metainfo.json file. The `info_columnas` is in turn a dictionary with the following attributes:

| Attribute         | Description                                                                                                                     | Options                                            |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| read_from         | Mode to read the width per column                                                                                               | "external_file","metainfo_file"                    |
| dir               | Complete direction where the external file is                                                                                   | e.g. "metainfo/DIGEVO_Estructura Interfazces.xlsx" |
| hoja              | Specify the sheet where we can take the information                                                                             | e.g. "RAW"                                         |
| primera_fila      | Specify the first row where the information starts, <br>without consider the header.                                            | e.g. 13                                            |
| loc_nombres_campo | Specify the column where are the names of each field                                                                            | e.g. "C"                                           |
| loc_intervalos    | Specify the column where are the interval of each field.<br>This interval can be in the same column or split in <br>two columns | e.g. "G" (one column), "G:H" (two columns)         |
| estilo_intervalos | Specify what is the style of the intervals that are read.                                                                       | "close-close", "close-open"                        |
| indice_inicial    | Specify the initial index in the way that are enumerated the intervals                                                          | 0, 1                                               |

One example of this attribute is 

```json
    "info_columnas" : {
        "read_from" : "external_file",
        "dir" : "metainfo/DIGEVO_Estructura Interfazces.xlsx",
        "hoja" : "RAW",
        "primera_fila" : 13,
        "loc_nombres_campo" : "C",
        "loc_intervalos" : "G:H",
        "estilo_intervalos" : "close-close",
        "indice_inicial" : 1
    }, 
```

You can also set the width per column directly. To do that use
`loc_ancho` instead of `loc_nombras_campo` and `estilo_intervalos`.

#### **Loading within the same metainfo file**

To read width or intervals per column, you can use `info_columnas` with the following attributes:

| Attribute         | Description                                                            | Options                         |
|-------------------|------------------------------------------------------------------------|---------------------------------|
| read_from         | Mode to read the width per column                                      | "external_file","metainfo_file" |
| estilo_intervalos | Specify what is the style of the intervals that are read.              | "close-close", "close-open"     |
| indice_inicial    | Specify the initial index in the way that are enumerated the intervals | 0, 1                            |
| columnas          | Specify the width or interval information per column                   | see example                     |

An example of this `info_columnas` is the following:

```json

    "info_columnas" : {
        "read_from" : "metainfo_file",
        "indice_inicial" : 1,
        "estilo_intervalos" : "close-open",
        "columnas" : [
            {
                "nombre_columna" : "Campo003",
                "intervalo" : [10,25]
            },
            {
                "nombre_columna" : "Campo004",
                "intervalo" : [25,65]
            }
        ]
    },
    
```

You can also you the attribute `ancho` per column to specify the width of the column, but the columns must be continuos. For example:

```json

    "info_columnas" : {
        "read_from" : "metainfo_file",
        "indice_inicial" : 1,
        "columnas" : [
            {
                "nombre_columna" : "Campo003",
                "ancho" : 5
            },
            {
                "nombre_columna" : "Campo004",
                "ancho" : 4
            }
        ]
    },
    
```

## Form Files - Metainfo Style

### Excel Form or xlsx Form Files Attributes

