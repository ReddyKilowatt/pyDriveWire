from ctypes import *
from struct import *


def dwCrc16(data):
    checksum = sum(bytearray(data))
    crc16 = pack(">H", c_ushort(checksum).value)
    return crc16

# vim: ts=4 sw=4 sts=4 expandtab
