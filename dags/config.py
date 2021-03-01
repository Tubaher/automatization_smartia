
#Directory where the temporal files will be stored
TMP_FILES_DIR = "stuff/tmp"

db_credential_postgress = {
    "provider" : "postgresql+psycopg2",
    "user" : "aztozcoembeuas",
    "password" : "37db8b9f5f174d1a58e6f910c9f6114d12bef8320b37d977a5df166d805c5198",
    "host" : "ec2-54-144-251-233.compute-1.amazonaws.com",
    "database" : "dat9k5tq31vohf",
}

db_credential_sqlserver = {
    "provider" : "mssql+pyodbc",
    "user" : "testSmartia",
    "password" : "1234567890",
    "host" : "192.168.100.26",
    "port" : "1433",
    "database" : "smartia",
    "driver" : "/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.1.1"
}

# Standard tables which are in the database 
# The datatypes are defined according one of the following types
# int32, int64, float32, float64, string, boolean, object
# Columns with mixed types are stored with the object dtype
TABLES_FIELDS = {
    "usuarios" : { "id"        : "int64" , 
                   "nombres"   : "string" , 
                   "apellidos" : "string" , 
                   "genero"    : "string" ,
                   "condicion" : "string" ,
                   "equipo"    : "int64"  , 
                   "cedula"    : "int64"  , 
                   "trabajo"   : "string" ,
                   "lugar"     : "string" },
                   
    "personas" : {  "rut"     : "int64",
                    "nombre"  : "string",
                    "supervisor" : "string",
                    "prioridad" : "int64",
                    "sum_saldos" : "float64"
                }            
}

# Define the operations between columns
OPERATIONS = {
    "+" : lambda col1, col2: col1 + col2,
    "-" : lambda col1, col2: col1 - col2
}