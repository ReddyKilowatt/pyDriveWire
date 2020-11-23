@echo off
REM run pydrivewire in Python 3 (port 65503) using the config file for the Python3 version of pyDriveWire.py
REM run with a remote REPL
REM python pyDriveWire.py -d -a -p 65503 --cmd-port 6809
REM python pyDriveWire.py --config c:\Users\z48176zz\.pydrivewirerc_py3  3dbrick.dsk
python pyDriveWire.py --config c:\Users\z48176zz\.pydrivewirerc_py3 %1
