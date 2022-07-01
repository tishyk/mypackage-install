import pytest

@pytest.fixture
def path1():
    yield 'path1 here'

@pytest.fixture
def path2():
    yield 'path1 here'
