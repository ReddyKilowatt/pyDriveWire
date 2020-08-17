#!python
import socket
# import threading
import sys

# sys.path.append("..")

# Mac dev path
# sys.path.append('/Users/tonycappellini/work/repos/git/pyDriveWire_3.6')

# Windows Dev path
sys.path.append(r'c:\Users\z48176zz\Documents\sources\GIT\Python\Coco\pyDriveWire3.7')
from dwconstants import *
from dwutil import *
from struct import *
# from ctypes import *

import time

PYTHON3_PORT = 65503


def pause(msg=''):
    input('\nPRESS ENTER\n')


def worker(cs):
    try:
        while True:
            data = cs.recv(192)
            dl = len(data)
            print(dl)
            if dl > 0:
                written = 0
                while written < dl:
                    written += cs.send(data[written:])
            else:
                print("Connection dropped.")
                break
    finally:
        print("Listening again...")


if len(sys.argv) < 2:
    print('ERROR: You must pass the name of a disk image as an argument')
    exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen = False
if listen:
    # print("Listening on port 65504...")
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
    # assert(ord(data) == 0xff)
    # assert (data == 0xff) # python3
    assert (data == b'\xff')  # python3
    disk = 0
    # input('About to check disk\n"s')
    for fileName in sys.argv[1:]:
        print(("Checking: %s" % fileName))
        # f = open(fileName)
        f = open(fileName, 'rb')  # Python3
        rc = E_OK
        lsn = 0
        while rc == E_OK:
            fd = f.read(256)
            fc = dwCrc16(fd)  # data coming back on first loop matches Python 2  b'\xff\x00'
            print(f'fc:{fc}, len(fc):{len(fc)}')
            # send command
            cs.send(OP_READEX)

            # send disk number
            cs.send(pack(">I", disk)[-1:])

            # send lsn
            cs.send(pack(">I", lsn)[-3:])

            data = cs.recv(256)
            print(f'data:{data}\nlen of data received: {len(data)}')
            # pause()
            sc = dwCrc16(data)
            # print(f'sc={sc}, len of sc:{len(sc)}')
            # Write the CRC
            cs.send(sc)
            # Get the RC
            # rc = ord(cs.recv(1))
            rc = cs.recv(1)  # Python 3
            print(f'rc=cs.recv(1){rc}')
            print(("lsn=%d fc=%s sc=%s" % (lsn, hex(unpack(">H", fc)[0]), hex(unpack(">H", sc)[0]))))
            assert (fc == sc)
            # print(("OP_READEX lsn %d len %d %d" % (lsn, len(data), rc)))
            print((f'OP_READEX lsn {lsn} len {len(data)} {rc}'))
            # msg = "%d ..." % lsn
            # msg+'\b'*len(msg),
            # print ".",
            lsn += 1

        # print(("\nCompared %d sectors rc %d" % (lsn, rc)))
        print((f'\nCompared {lsn} sectors rc {rc}'))
        # assert (rc in [E_OK, E_EOF])
        f.close()
