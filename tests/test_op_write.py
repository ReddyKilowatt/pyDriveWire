#!python
import socket
import sys

# Mac dev path
# sys.path.append('/Users/tonycappellini/work/repos/git/pyDriveWire_3.6')

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


#
#
# def test_print_name(disk_name):
#     print(f"\ncommand line param (disk_name): {disk_name}")
#
#
# def test_print_name_2(pytestconfig):
#     print(f"test_print_name_2(disk_name): {pytestconfig.getoption('disk_name')}")


def server_command(cmd):
    """
    Uses the telnet server to send commands to the main pyDriveWire server
    """
    socket = dwsocket.DWSocket(port=6809)
    socket.debug = True
    socket.connect()
    # socket.write('dw disk show\n')  # <- the NEWLINE IS absolutely necessary
    socket.write('f{cmd}\n')  # <- the NEWLINE IS absolutely necessary
    # print(socket.read())
    socket.close()
    return socket


def create_disk(drive_number, disk_name):
    socket = server_command(f'dw disk create {drive_number} {disk_name}')
    show_disk(socket, drive_number)


def show_disk(socket, drive_number):
    server_command(f'dw disk show {drive_number}')
    print(socket.read())


def diskwrite(disk_name, cs):
    """
    0	OP_WRITE ($57)
    1	Drive number (0-255)
    2	Bits 23-16 of of 24-bit Logical Sector Number (LSN
    3	Bits 15-8 of LSN
    4	Bits 7-0 of LSN
    5-260	256 bytes of sector data to write
    261	Bits 15-8 of checksum (computed by CoCo)
    262	Bits 7-0 of checksum (computed by CoCo)
    """

    # open a disk image to read
    # read 1 sector at a time
    # write the data to the server
    # continue until all sectors have been written

    # write the contents of the server to a new disk file
    # manually diff the two files (for now) to see if they compare

    # create_disk(254,'junk.dsk')

    with open(disk_name, 'rb') as fh_in:
        rc = E_OK
        lsn = 0
        drive_number = 0  # TODO make a cmd line arg or pytest fixture control
        while rc == E_OK: # TODO && lsn < the max sectors for the disk type (passed in on cmd line)
            print(f'Write LSN: {lsn}')
            read_data = fh_in.read(COCO_SECTOR_SIZE)
            rc = write_sector(cs, lsn, drive_number, read_data)
            lsn += 1

        print(f"Finished writing {lsn - 1} sectors")
    return rc, lsn


def read_sector(cs, fh_in, lsn, drive_number):
    disk_data = fh_in.read(COCO_SECTOR_SIZE)
    disk_checksum = dwCrc16(disk_data)  # data coming back on first loop matches Python 2  b'\xff\x00'
    # TODO use the python logger instead of print()
    print(f'disk_checksum:{disk_checksum}')

    # Send opcode of next cmd to DW server
    # DW SPEC: Readex is a 5-byte transaction
    cs.send(OP_READEX)  # Readex Byte 0
    # send disk number  # DW SPEC: must be 0-255
    cs.send(pack(">I", drive_number)[-1:])  # Readex Byte 1
    # send lsn
    cs.send(pack(">I", lsn)[-3:])  # Readex Bytes 2,3,4

    server_data = cs.recv(COCO_SECTOR_SIZE)
    # print(f'data:{server_data}\nlen of data received: {len(server_data)}')
    server_checksum = dwCrc16(server_data)
    # Write the CRC
    cs.send(server_checksum)
    # Get the RC
    rc = cs.recv(1)  # Python 3
    print(f'rc={rc}, lsn={lsn} disk_crc={hex(unpack(">H", disk_checksum)[0])} server_crc={hex(unpack(">H", server_checksum)[0])}\n')
    assert (disk_checksum == server_checksum)
    return rc


def write_sector(cs, lsn, drive_number, data):
    cs.send(OP_WRITE)

    # Drive Number - 1 Byte
    cs.send(pack(">I", drive_number)[-1:])
    # LSN - 3 Bytes
    cs.send(pack(">I", lsn)[-3:])
    cs.send(data)
    disk_checksum = dwCrc16(data)
    cs.send(disk_checksum)
    rc = cs.recv(1)
    print(f'rc={rc}')  # TODO control the printing of this with the Python Logger
    return rc


def server_init(cs):
    print("s")
    cs.send(OP_DWINIT)
    cs.send(b'A')
    data = cs.recv(1)
    print("r")
    return data


def socket_init():
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


def test_opwrite(disk_name):
    """
    This is the top-level test function called by pytest
    All values tested by pytest are tested here, so that the user only needs to look in one place
    to get an overview of what the test is doing.
    """
    rc = E_OK

    cs = socket_init()
    assert cs is not None, 'ERROR: test_opwrite(): Socket initialization was not successfull\n'

    init_data = server_init(cs)
    assert init_data == b'\xff', f'test_opwrite(): DWINIT ERROR: Server initialization was not successful. Data from recv() was' \
                                 f' {init_data}, exp: b"\xff" \n'

    rc, lsn = diskwrite(disk_name, cs)
    assert rc != E_OK, f'test_opwrite(): diskwrite() test returned {rc}'

    # TODO lsn number needs to be passed in on the cmd line , depending on the disk type
    # assert lsn < COCO_SECTOR_SIZE, f'test_opwrite(): diskwrite() lsn was {lsn}, EXP < {COCO_DISK_SECTOR_SIZE}.\n'


@pytest.fixture()
def disk_name(pytestconfig):
    """
    When running this test, disk_name must be passed to pytest, NOT the test itself:
    pytest --disk_name 3dbrick.dsk test_op_write.py

    This is needed to get the filename passed on the cmd line with the disk_name argument
    and return it to the fixture, so that disk_name is passted to test_opwrite() as its
    argument.
    """
    return pytestconfig.getoption("disk_name")
