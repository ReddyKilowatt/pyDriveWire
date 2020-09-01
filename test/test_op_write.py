#!python
import argparse
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


def test_diskwrite(disk_name, cs):
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

    with open(disk_name, 'rb') as fh_in:
        rc = E_OK
        lsn = 0
        drive_number = 0
        while rc == E_OK:
            # rc, read_data, read_chksum = read_sector(cs, fh_in, lsn, drive_number)
            read_data = fh_in.read(COCO_DISK_SECTOR_SIZE)
            write_sector(cs, lsn, drive_number, read_data)
            lsn += 1

        print(f"Finished writing {lsn} sectors")


def read_sector(cs, fh_in, lsn, drive_number):
    disk_data = fh_in.read(COCO_DISK_SECTOR_SIZE)
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

    server_data = cs.recv(COCO_DISK_SECTOR_SIZE)
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
    disk_checksum = dwCrc16(data)
    cs.send(data)
    cs.send(disk_checksum)

    # ???
    # Get the RC
    rc = cs.recv(1)  # Python 3
    # print(f'rc={rc}, lsn={lsn} disk_crc={hex(unpack(">H", disk_checksum)[0])} server_crc={hex(unpack(">H", disk_checksum)[0])}\n')


def server_init(cs):
    print("s")
    cs.send(OP_DWINIT)
    cs.send(b'A')
    data = cs.recv(1)
    print("r")
    assert (data == b'\xff')


def socket_init():
    # TODO Add exception handling
    # ConnectionRefusedError:
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
            port = PYTHON3_PORT
            cs = socket.create_connection((addr, port))
            print("connection to : %s:%s" % (addr, port))
    return cs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=argparse.FileType('r'), nargs='+')
    parsed_args = parser.parse_args()

    cs = socket_init()
    if cs is not None:
        server_init(cs)
        for ioWrapperObj in parsed_args.file_name:
            test_diskwrite(ioWrapperObj.name, cs)
    else:
        print('ERROR: Socket initialization was not successfull\n')


main()
