# from Mike Furman on 8/31/2020 in Discord
# this code sends a command to the DW server on a different
# port # thn the server is running on. It also uses a different
# socket connection than the sockets in the test programs that I wrote

# This is the fundamental flaw I had with my thinking- that I could
# use the same socket as those in the test program

import sys
sys.path.append('..')
import dwsocket
# from dwsocket import DWSocket
s = dwsocket.DWSocket(port=6809)
s.debug = True
s.connect()
s.write('dw disk show\n')
print(s.read())
s.close()

# def create_disk(drive_number, disk_name):
#     socket = server_command(f'dw disk create {drive_number} {disk_name}')
#     show_disk(socket, drive_number)

# def show_disk(socket, drive_number):
#     server_command(f'dw disk show {drive_number}')
#     print(socket.read())

