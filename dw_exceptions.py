
class DWBaseException(Exception):
    """
    Base class for all future DW exception classes.
    This class is not providing much functionality ATM,
    but provides a convenient way to add new functionality to all derived
    exception classes in the future.
    """

    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class DWDriveNumberError(DWBaseException):
    """
    Raised when a floppy drive number is < 0 or > 3
    """
    def __init__(self, reason):
        DWBaseException.__init__(self, reason)
