import os
import tempfile

import pytest

from src.aircraft import Aircraft
from src.aircraft_storage import AircraftStorageJSON


@pytest.fixture
def aircraft1():
    return Aircraft(id_board="39de4f", callsign="TVF19TV", country="France", velocity=224.22, height=10942.32)


@pytest.fixture
def aircraft2():
    return Aircraft(id_board="ab6fdd", callsign="AAL960", country="United States", velocity=60.39, height=739.14)


@pytest.fixture
def aircraft3():
    return Aircraft(id_board="a3feee", callsign="N357BG", country="Ireland", velocity=341.81, height=12184.38)


@pytest.fixture
def temp_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def storage(temp_file):
    return AircraftStorageJSON(temp_file)
