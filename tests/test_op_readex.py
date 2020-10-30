#!python

import socket
import sys

import pytest

# Mac dev path
# sys.path.append('/Users/tonycappellini/work/repos/git/pyDriveWire_3.6')

# Windows Dev path
sys.path.append(r'c:\Users\z48176zz\Documents\sources\GIT\Python\Coco\pyDriveWire3.7')

from dwconstants import *
from dwutil import *
from struct import *

from coco_constants import *

PYTHON3_PORT = 65503


def disk_read(disk_image, drive_number, cs):
    rc = E_OK
    with open(disk_image, 'rb') as fh:
        rc = E_OK
        lsn = 0
        while rc == E_OK:  # TODO && lsn < the max sectors for the disk type (passed in on cmd line)
            rc = read_sector(cs, fh, lsn, drive_number)
            lsn += 1
        # print((f'Compared {lsn} sectors, rc={rc}'))
        print(f"Finished reading {lsn - 1} sectors")
    return rc, lsn


def read_sector(cs, fh_in, lsn, drive_number):
    # TODO exception handling for I/O ERRORS
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


def test_opreadex(disk_name):
    cs = socket_init()
    assert cs is not None, 'ERROR: test_opreadex(): Socket initialization was not successfull\n'
    init_data = server_init(cs)
    assert init_data == b'\xff', f'test_opreadex(): DWINIT ERROR: Server initialization was not successful. Data from recv() was' \
                                 f' {init_data}, exp: b"\xff" \n'

    drive_number = 0
    rc, lsn = disk_read(disk_name, drive_number, cs)
    assert rc != E_OK, f'test_opreadex(): disk_read() test returned {rc}'

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
