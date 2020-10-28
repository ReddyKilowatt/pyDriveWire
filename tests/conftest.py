import pytest


# https://stackoverflow.com/questions/40880259/how-to-pass-arguments-in-pytest-by-command-line
def pytest_addoption(parser):
    parser.addoption("--disk_name", action="store", default="default disk_name")
