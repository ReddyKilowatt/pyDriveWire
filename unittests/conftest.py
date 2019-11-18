"""
Adding cmd line args to unit tests
https://stackoverflow.com/questions/40880259/how-to-pass-arguments-in-pytest-by-command-line
"""
# conftest.py


def pytest_addoption(parser):
    """
    Adds the --name argument to the parser for other test files in the same directory
    :param parser:
    :return:
    """
    # parser.addoption("--name", action="store")
    parser.addoption("--filename", action="store")
