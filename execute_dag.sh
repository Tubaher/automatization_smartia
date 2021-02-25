DIR_CONFIG="metainfo/metainfo_excel_sample.json"
dict_params="{\"cfg_file\":\"${DIR_CONFIG}\"}"

airflow trigger_dag 'pandas_dag' -r 'excel_sample' --conf $dict_params
