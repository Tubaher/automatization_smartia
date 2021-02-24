DIR_CONFIG="config_files/metainfo_excel_sample.json"
dict_params="{\"cfg_file\":\"${DIR_CONFIG}\"}"

airflow tasks test pandas_dag $1 2021-02-22 -t $dict_params