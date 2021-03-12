#!/bin/bash

DIR_METAFILES="metainfo/"
declare -a FILES_TO_TEST=("metainfo_csv_alterado_sample.json" \
                      "metainfo_csv_sample.json" \
                      "metainfo_excel_sample.json" \
                      "metainfo_fijo_sample_ext_file.json" \
                      "metainfo_fijo_sample.json" \
                      "metainfo_form.json")

dict_params="{\"cfg_file\":\"${DIR_CONFIG}\"}"

PATH="${2}metainfo*"

exit_if_error() {
  local exit_code=$1
  shift
  [[ $exit_code ]] &&               # do nothing if no error code passed
    ((exit_code != 0)) && {         # do nothing if error code is 0
      printf 'ERROR: %s\n' "$@" >&2 # we can use better logging here
      exit "$exit_code"             # we could also check to make sure
                                    # error code is numeric when passed
    }
}

for meta_file in ${FILES_TO_TEST[@]}; do
    
    # dict_params="{\"cfg_file\":\"${meta_file}\"}"
    echo " "
    echo "-----------"
    meta_file_dir="${DIR_METAFILES}${meta_file}"
    echo "METAFILE DIR ${meta_file_dir}"
    echo "Running: ./execute_task_tables ${1} ${meta_file}"
    source execute_task_tables.sh load_table $meta_file_dir || exit_if_error $? "Test case ${meta_file} failed"

    # ./execute_task_tables $1 $meta_file || exit_if_error $? "Test case ${meta_file} failed"

done

