# DIR_CONFIG="metainfo/metainfo_excel_sample.json"
dict_params="{\"cfg_file\":\"${3}\"}"
id=$2
id_name="{${1}_id_${2}}"

airflow trigger_dag $1 -r $id_name --conf $dict_params
