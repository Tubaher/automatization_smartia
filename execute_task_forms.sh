#DIR_CONFIG="metainfo/metainfo_excel_sample.json"
#dict_params="{\"cfg_file\":\"${DIR_CONFIG}\"}"

dict_params="{\"cfg_file\":\"${2}\"}"

airflow tasks test forms_dag $1 2021-02-22 -t $dict_params