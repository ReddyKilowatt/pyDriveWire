from ctypes import *
from struct import *


def dwCrc16(data):
    checksum = sum(bytearray(data))
    return pack(">H", c_ushort(checksum).value) # this is already a bytes type

# vim: ts=4 sw=4 sts=4 expandtab
