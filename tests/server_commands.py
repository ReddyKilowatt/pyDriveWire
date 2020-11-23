from remote_repl import RemoteRepl


class ServerCommand:
    def __init__(self, debug_opt):
        self._repl = RemoteRepl(debug=debug_opt)
        self._write = self.repl.write
        self._read = self.repl.read

    def disk_show(self):
        self._write('dw disk show')
        read_data = self._read()
        print(f'{read_data}')
        # return read_data
