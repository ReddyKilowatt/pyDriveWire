
# XXX: convert to b'\xff' format, replace chr()
# TODO go here
OP_RESET3 = chr(0xF8).encode('UTF-8')
OP_RESET2 = chr(0xFE).encode('UTF-8')
OP_RESET1 = chr(0xFF).encode('UTF-8')
OP_INIT = chr(0x49).encode('UTF-8')
OP_TERM = chr(0x54).encode('UTF-8')
OP_DWINIT = chr(0x5A).encode('UTF-8')
OP_TIME = chr(0x23).encode('UTF-8')
OP_NOP = chr(0x00).encode('UTF-8')
OP_READ = chr(0x52).encode('UTF-8')
OP_REREAD = chr(0x72).encode('UTF-8')
OP_WRITE = chr(0x57).encode('UTF-8')
OP_READEX = chr(0xD2).encode('UTF-8')
OP_REREADEX = chr(0xF2).encode('UTF-8')
OP_REWRITE = chr(0x77).encode('UTF-8')
OP_GETSTAT = chr(0x47).encode('UTF-8')
OP_SETSTAT = chr(0x53).encode('UTF-8')
OP_PRINT = chr(0x50).encode('UTF-8')
OP_PRINTFLUSH = chr(0x46).encode('UTF-8')
OP_SERINIT = chr(0x45).encode('UTF-8')
OP_SERREAD = chr(0x43).encode('UTF-8')
OP_PRINTFLUSH = chr(0x46).encode('UTF-8')
OP_PRINT = chr(0x50).encode('UTF-8')
OP_SERREADM = chr(0x63).encode('UTF-8')
OP_SERWRITE = chr(0xC3).encode('UTF-8')
OP_FASTWRITE0 = chr(0x80).encode('UTF-8')
OP_FASTWRITE1 = chr(0x81).encode('UTF-8')
OP_FASTWRITE2 = chr(0x82).encode('UTF-8')
OP_FASTWRITE3 = chr(0x83).encode('UTF-8')
OP_FASTWRITE4 = chr(0x84).encode('UTF-8')
OP_FASTWRITE5 = chr(0x85).encode('UTF-8')
OP_FASTWRITE6 = chr(0x86).encode('UTF-8')
OP_FASTWRITE7 = chr(0x87).encode('UTF-8')
OP_FASTWRITE8 = chr(0x88).encode('UTF-8')
OP_FASTWRITE9 = chr(0x89).encode('UTF-8')
OP_FASTWRITE10 = chr(0x8A).encode('UTF-8')
OP_FASTWRITE11 = chr(0x8B).encode('UTF-8')
OP_FASTWRITE12 = chr(0x8C).encode('UTF-8')
OP_FASTWRITE13 = chr(0x8D).encode('UTF-8')
OP_FASTWRITE14 = chr(0x8E).encode('UTF-8')
OP_FASTWRITE15 = chr(0x8F).encode('UTF-8')
OP_SERWRITEM = chr(0x64).encode('UTF-8')
OP_SERGETSTAT = chr(0x44).encode('UTF-8')
OP_SERSETSTAT = chr(0xC4).encode('UTF-8')
OP_SERTERM = chr(0xC5).encode('UTF-8')


E_OK = 0
E_EOF = 211
E_WRPROT = 242
E_CRC = 243
E_READ = 244
E_WRITE = 245
E_NOTRDY = 246
E_SEEK = 247

NULL = chr(0).encode('UTF-8')

SECSIZ = 256
INFOSIZ = 4
CRCSIZ = 2
STATSIZ = 2

SS_ComSt = chr(0x28).encode('UTF-8')
SS_Open = chr(0x29).encode('UTF-8')
SS_Close = chr(0x2A).encode('UTF-8')

# EmCee Protocol
MC_ATTENTION = chr(0x21).encode('UTF-8')
MC_LOAD = chr(0x4C).encode('UTF-8')
MC_GETBLK = chr(0x47).encode('UTF-8')
MC_NXTBLK = chr(0x4E).encode('UTF-8')
MC_SAVE = chr(0x53).encode('UTF-8')
MC_WRBLK = chr(0x57).encode('UTF-8')
MC_OPEN = chr(0x4F).encode('UTF-8')
MC_DIRFIL = chr(0x46).encode('UTF-8')
MC_RETNAM = chr(0x24).encode('UTF-8')
MC_DIRNAM = chr(0x44).encode('UTF-8')
MC_SETDIR = chr(0x43).encode('UTF-8')
MC_REWRBLK = chr(0x77).encode('UTF-8')
MC_PRINT = chr(0x50).encode('UTF-8')

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
