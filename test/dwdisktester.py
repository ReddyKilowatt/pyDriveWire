#!python
import socket
import sys

# Mac dev path
# sys.path.append('/Users/tonycappellini/work/repos/git/pyDriveWire_3.6')

# Windows Dev path
sys.path.append(r'c:\Users\z48176zz\Documents\sources\GIT\Python\Coco\pyDriveWire3.7')

from dwconstants import *
from dwutil import *
from struct import *

PYTHON3_PORT = 65503
COCO_DISK_SECTOR_SIZE = 256

if len(sys.argv) < 2:
    print('ERROR: You must pass the name of a disk image as an argument')
    exit(1)
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
        port = PYTHON3_PORT
        cs = socket.create_connection((addr, port))
        print("connection to : %s:%s" % (addr, port))

    print("s")
    cs.send(OP_DWINIT)
    cs.send(b'A')
    data = cs.recv(1)
    print("r")
    assert (data == b'\xff')  # python3

    disk = 0
    for fileName in sys.argv[1:]:
        print(("Checking Disk: %s" % fileName))
        f = open(fileName, 'rb')  # Python3
        rc = E_OK
        lsn = 0
        while rc == E_OK:
            disk_data = f.read(COCO_DISK_SECTOR_SIZE)
            disk_checksum = dwCrc16(disk_data)  # data coming back on first loop matches Python 2  b'\xff\x00'
            print(f'disk_checksum:{disk_checksum}')

            # Send opcode of next cmd to DW server
            # DW SPEC: Readex is a 5-byte transaction
            cs.send(OP_READEX)  # Readex Byte 0
            # send disk number  # DW SPEC: must be 0-255
            cs.send(pack(">I", disk)[-1:])  # Readex Byte 1
            # send lsn
            cs.send(pack(">I", lsn)[-3:])  # Readex Bytes 2,3,4

            server_data = cs.recv(COCO_DISK_SECTOR_SIZE)
            # print(f'data:{server_data}\nlen of data received: {len(server_data)}')
            server_checksum = dwCrc16(server_data)
            # Write the CRC
            cs.send(server_checksum)
            # Get the RC
            rc = cs.recv(1)  # Python 3
            print(f'rc={rc}, lsn={lsn} disk_crc={hex(unpack(">H", disk_checksum)[0])} server_crc={hex(unpack(">H", server_checksum)[0])}\n')
            assert (disk_checksum == server_checksum)
            lsn += 1

        print((f'\nCompared {lsn} sectors rc={rc}'))
        f.close()
