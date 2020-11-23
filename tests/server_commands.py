from remote_repl import RemoteRepl


class ServerConfigCommands:

    def _config_common(self, repl_command, print_output=True):
        self._write(f'dw config {repl_command}')
        data = self._read()
        if print_output:
            print(f'{data}')
        return data  # the caller may want to parse the output for specific content

    def config_show(self, print_output=True):
        return self._config_common('show', print_output)


class ServerDiskCommands:

    def _disk_common(self, repl_command, print_output=True):
        self._write(f'dw disk {repl_command}')
        data = self._read()
        if print_output:
            print(f'{data}')
        return data  # the caller may want to parse the output for specific content

    def disk_show(self, print_output=True):
        return self._disk_common('show', print_output)

    def disk_create(self, drive_number, disk_filename):
        return self._disk_common(f'disk {drive_number} {disk_filename}')

    def disk_eject(self, drive_number):
        return self._disk_common(f'disk eject {drive_number}')

    def disk_insert(self, drive_number, path):
        return self._disk_common(f'disk insert {drive_number} {path}')

    def disk_info(self, drive_number):
        return self._disk_common(f'disk info {drive_number}')


class ServerCommand(ServerDiskCommands, ServerConfigCommands):
    """
    The ServerCommand class provides a simple way for the caller
    to send commands to the pyDriveWire server
    """

    def __init__(self, debug_opt=False):
        self._repl = RemoteRepl(debug=debug_opt)
        self._write = self._repl.write
        self._read = self._repl.read


sc = ServerCommand()
# sc.config_show()
sc.disk_show()
