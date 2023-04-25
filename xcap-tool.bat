@echo off
SET PYTHONPATH=%PYTHONPATH%;"C:\Repository\nf_registration_tool"

python .\src\nf_registration_tool.py %*
