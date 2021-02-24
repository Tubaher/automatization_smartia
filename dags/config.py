
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

# Tablas estandar que existen en la base de datos
TABLES_FIELDS = {
    "usuarios" : ["id", "nombres", "apellidos", "genero", "condicion", 
                    "equipo", "cedula", "trabajo", "lugar" ]
}
