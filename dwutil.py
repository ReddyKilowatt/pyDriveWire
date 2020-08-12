from ctypes import *
from struct import *


def dwCrc16(data):
    print(f'dwCrc16({type(data)}')
    checksum = sum(bytearray(data))
    print(f'checksum={checksum}')
    # return pack(">H", c_ushort(checksum).value) # this is already a bytes type
    crc16 = pack(">H", c_ushort(checksum).value)
    print(f'crc16={crc16}')
    return crc16

# vim: ts=4 sw=4 sts=4 expandtab
