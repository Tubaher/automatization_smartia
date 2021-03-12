#DIR_CONFIG="metainfo/metainfo_excel_sample.json"
#dict_params="{\"cfg_file\":\"${DIR_CONFIG}\"}"

PATH="${2}metainfo*"

FAILED=0
PASSED=0

for meta_file in $PATH; do
    echo $meta_file
    dict_params="{\"cfg_file\":\"${meta_file}\"}"

    {
    airflow tasks test table_dag $1 2021-02-22 -t $dict_params
    PASSED=$(( PASSED + 1 ))
    echo "Passed: ${meta_file}"
    } || { 
    echo "Failed: ${meta_file}"
    FAILED=$(( FAILED + 1 ))
    }
done

echo "PASSED: ${PASSED} and FAILED: ${FAILED}"
