#!/usr/bin/env bash

TOOL=/home/xgntools/T23AJ001/src/xcap_tool.py
export PYTHONPATH=${PYTHONPATH}:/home/xgntools/T23AJ001/

# execute xcap_tool.py
python3 -O ${TOOL} "${@}"
EXIT_CODE=${?}

exit ${EXIT_CODE}
