#!/usr/bin/env bash

TOOL=/home/xgntools/T2xAJ001/src/xcap_tool.py
export PYTHONPATH=${PYTHONPATH}:/home/xgntools/T2xAJ001/

# execute nf_registration_tool.py
python3 -O ${TOOL} "${@}"
EXIT_CODE=${?}

exit ${EXIT_CODE}
