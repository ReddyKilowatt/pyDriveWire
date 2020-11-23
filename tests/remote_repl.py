import sys

sys.path.append('..')  # the DW imports are in the parent dir
import dwsocket


class RemoteRepl:
    def __init__(self, debug=False, repl_port=6809):
        self.repl_port = repl_port
        self.debug = debug
        self.socket = dwsocket.DWSocket(port=self.repl_port)
        self.socket.debug = self.debug
        self.socket.connect()  # timeout? Exception handler??

    def debug_off(self):
        self.socket.debug = False

    def debug_on(self):
        self.socket.debug = True

    def write(self, repl_cmd):
        self.socket.write(f'{repl_cmd}\n')  # the \n is CRITICAL !!!

    def read(self):
        # TODO Exceptions to catch ??
        data = self.socket.read()
        self.socket.close()
        return data
