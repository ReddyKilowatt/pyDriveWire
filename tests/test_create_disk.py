#!python
import socket
import sys
import time

# Windows Dev path
sys.path.append(r'c:\Users\z48176zz\Documents\sources\GIT\Python\Coco\pyDriveWire3.7')

import dwsocket
from dwconstants import *
from dwutil import *
from struct import *
from coco_constants import *

PYTHON3_PORT = 65503  # This allows running a Python 2.7 server on 65502, concurrently with a Python 3 server

"""
THIS CODE CAN BE USED TO SEND COMMANDS TO THE'SERVER WITHOUT NEEDING
TO TYPE THE COMMANDS IN THE SERVER CONSOLE
TO USE IT option cmdPort 6809 must be in the .pydrivewire_py3 file


import sys
sys.path.append('..')
import dwsocket
from dwsocket import DWSocket
s = dwsocket.DWSocket(port=6809)
s.debug = True
s.connect()
s.write('dw disk show\n')  # <- the NEWLINE IS absolutely necessary
print(s.read())
s.close()
"""

import pytest


def rr_init_socket(port=REMOTE_REPL_PORT):
    socket = None
    try:
        socket = dwsocket.DWSocket(port)
        socket.debug = True
        _ = socket.connect()
    except TypeError:
        print('FATAL ERROR in init_socket')

    return socket


def server_command(socket, cmd):
    """
    Uses the telnet server to send commands to the main pyDriveWire server
    """
    print('server_command()\n')

    server_cmd = f'{cmd}\n'  # <- the NEWLINE IS absolutely necessary
    _ = socket.write(server_cmd.encode('utf-8'))  # need to do this in the server


def create_disk(socket, drive_number, dest_disk_name):
    print('create_disk()\n')
    print(f'Creating blank disk image "{dest_disk_name}" on drive # {drive_number}\n')
    try:
        server_command(socket, f'dw disk create {drive_number} {dest_disk_name}')
        print('After creating socket\n')
    except Exception:
        raise  # so the caller sees it, and we can catch the specific exception


def eject_disk(socket, drive_number, dest_disk_name):
    print('eject_disk()\n')
    print(f'Ejecting disk image {dest_disk_name} on drive # {drive_number}\n')
    server_command(socket, f'dw disk eject {drive_number}')
    print('After creating socket\n')


def show_disk(socket):
    print('show_disk()\n')
    server_command(socket, f'dw disk show')
    print(socket.read())


def dw_server_init(cs):
    data = ''
    print('server_init()')
    print("s")
    cs.send(OP_DWINIT)
    cs.send(b'A')
    data = cs.recv(1)
    print("r")
    return data


def dw_socket_init():
    print('socket_init()')

    cs = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen = False
    if listen:
        print(f'Listening on PYTHON3 PORT: {PYTHON3_PORT} ...')
        # s.bind(('0.0.0.0', 65504))
        s.bind(('0.0.0.0', PYTHON3_PORT))
        s.listen(0)
    if True:
        if listen:
            (cs, addr) = s.accept()
            print("Accepted connection: %s" % str(addr))
        else:
            # addr = "172.16.1.89"
            # addr = "192.168.4.1"
            addr = '127.0.0.1'
            # port = 65504
            # port = PYTHON3_PORT + 1 # bad port for testing
            port = PYTHON3_PORT
            try:
                cs = socket.create_connection((addr, port))
            except ConnectionRefusedError:
                print(f'\n\nServer Connection Error: The server refused to connect on Addr: {addr}, Port: {port}. Please verify those '
                      f'values.\n')
            else:
                print(f'connection to : {addr}:{port}')
    return cs


def test_create_disk():
    """
    This is the top-level test function called by pytest
    All values tested by pytest are tested here, so that the user only needs to look in one place
    to get an overview of what the test is doing.
    """
    rc = E_OK
    dest_disk_name = 'newdisk.dsk'
    drive_number = 0

    dw_sock = dw_socket_init()
    dw_server_init(dw_sock)

    rr_socket = rr_init_socket()
    # assert rr_socket is None, "init_socket() was not successful"
    create_disk(rr_socket, drive_number, dest_disk_name)

    show_disk(rr_socket)
    print('\n\n\nSLEEP 5\n\n\n')
    time.sleep(5)
    eject_disk(rr_socket, drive_number, dest_disk_name)
    rr_socket.close()
    # assert rc == 0, "eject_disk() was not successful"
