import pytest


@pytest.fixture()
def name(pytestconfig):
    return pytestconfig.getoption("name")


def test_print_name(name):
    print(f"\ncommand line param (name): {name}")


def test_print_name_2(pytestconfig):
    print(f"test_print_name_2(name): {pytestconfig.getoption('name')}")
