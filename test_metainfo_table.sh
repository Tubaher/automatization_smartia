#DIR_CONFIG="metainfo/metainfo_excel_sample.json"
#dict_params="{\"cfg_file\":\"${DIR_CONFIG}\"}"

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

for meta_file in $PATH; do
    # dict_params="{\"cfg_file\":\"${meta_file}\"}"
    echo " "
    echo "-----------"
    echo "Running: ./execute_task_tables ${1} ${meta_file}"
    ./execute_task_tables $1 $meta_file || exit_if_error $? "Test case ${meta_file} failed"

done
