@echo off

REM run the read test just to make sure the server is setup correctly
REM pytest --disk_name 3dbrick.dsk tests\test_op_readex.py
pytest --disk_name 3dbrick.dsk tests\test_op_write.py
