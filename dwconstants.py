# XXX: convert to b'\xff' format, replace chr()
# TODO go here
OP_RESET3 = b'\xF8'
OP_RESET2 = b'\xFE'
# OP_RESET1 = chr(0xFF)
OP_RESET1 = b'\xFF'
OP_INIT = b'\x49'
OP_TERM = b'\x54'
# OP_DWINIT = chr(0x5A)
OP_DWINIT = b'\x5A'  # from Mike's message in Discord
OP_TIME = b'\x23'
OP_NOP = b'\x00'
OP_READ = b'\x52'
OP_REREAD = b'\x72'
OP_WRITE = b'\x57'
OP_READEX = b'\xD2'
OP_REREADEX = b'\xF2'
OP_REWRITE = b'\x77'
OP_GETSTAT = b'\x47'
OP_SETSTAT = b'\x53'
OP_PRINT = b'\x50'
OP_PRINTFLUSH = b'\x46'
OP_SERINIT = b'\x45'
OP_SERREAD = b'\x43'
OP_PRINTFLUSH = b'\x46'
OP_PRINT = b'\x50'
OP_SERREADM = chr(0x63)
OP_SERWRITE = chr(0xC3)
OP_FASTWRITE0 = chr(0x80)
OP_FASTWRITE1 = chr(0x81)
OP_FASTWRITE2 = chr(0x82)
OP_FASTWRITE3 = chr(0x83)
OP_FASTWRITE4 = chr(0x84)
OP_FASTWRITE5 = chr(0x85)
OP_FASTWRITE6 = chr(0x86)
OP_FASTWRITE7 = chr(0x87)
OP_FASTWRITE8 = chr(0x88)
OP_FASTWRITE9 = chr(0x89)
OP_FASTWRITE10 = chr(0x8A)
OP_FASTWRITE11 = chr(0x8B)
OP_FASTWRITE12 = chr(0x8C)
OP_FASTWRITE13 = chr(0x8D)
OP_FASTWRITE14 = chr(0x8E)
OP_FASTWRITE15 = chr(0x8F)
OP_SERWRITEM = chr(0x64)
OP_SERGETSTAT = chr(0x44)
OP_SERSETSTAT = chr(0xC4)
OP_SERTERM = b'\xC5'

# E_OK = 0
# E_EOF = 211
# E_WRPROT = 242
# E_CRC = 243
# E_READ = 244
# E_WRITE = 245
# E_NOTRDY = 246
# E_SEEK = 247

# Python 3
E_OK = b'\x00'
E_EOF = b'\xD3'
E_WRPROT = b'\xF2'
E_CRC = b'\xF3'
E_READ = b'\xF4'
E_WRITE = b'\xF5'
E_NOTRDY = b'\xF6'
E_SEEK = b'\xF7'

# NULL = chr(0)
# Python 3
NULL = b'\x00'

# SECSIZ = 256 # replaced with COCO_SECTOR_SIZE in coco_constants.py
INFOSIZ = 4
CRCSIZ = 2
STATSIZ = 2

# SS_ComSt = chr(0x28)
# SS_Open = chr(0x29)
# SS_Close = chr(0x2A)

SS_ComSt = b'\x28'
SS_Open = b'\x29'
SS_Close = b'\x2A'

# EmCee Protocol
MC_ATTENTION = chr(0x21)
MC_LOAD = chr(0x4C)
MC_GETBLK = chr(0x47)
MC_NXTBLK = chr(0x4E)
MC_SAVE = chr(0x53)
MC_WRBLK = chr(0x57)
MC_OPEN = chr(0x4F)
MC_DIRFIL = chr(0x46)
MC_RETNAM = chr(0x24)
MC_DIRNAM = chr(0x44)
MC_SETDIR = chr(0x43)
MC_REWRBLK = chr(0x77)
MC_PRINT = chr(0x50)

# EmCee Errors
E_MC_FC = 8
E_MC_IO = 34
E_MC_FM = 36
E_MC_DN = 38
E_MC_NE = 40
E_MC_WP = 42
E_MC_FN = 44
E_MC_FS = 46
E_MC_IE = 48
E_MC_FD = 50
E_MC_AO = 52
E_MC_NO = 54
E_MC_DS = 56

# vim: ts=4 sw=4 sts=4 expandtab
