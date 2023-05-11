#!/usr/bin/env bash

TOOL=/home/xgntools/T23AJ001/src/xcap_tool.py
export PYTHONPATH=${PYTHONPATH}:/home/xgntools/T23AJ001/

HEISOKUDB_TOOL=/home/xgntools/T8AJ001/T8AJ001_heisoku-db.sh
HEISOKU_LIST=$(${HEISOKUDB_TOOL} LISTW)
i=0
while [ "$1" != "" ] && [[ $1 != *"--"* ]]
do
    ARGV[i]=$1
    shift
    i=$((i + 1))
done

# execute xcap_tool.py
python3 -O ${TOOL} "${ARGV[@]}" "${HEISOKU_LIST}" "${@}"
EXIT_CODE=${?}

exit ${EXIT_CODE}
