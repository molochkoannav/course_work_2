import pytest
from src.aircraft import Aircraft

@pytest.fixture
def aircraft1():
    return Aircraft(
        id_board='39de4f',
        callsign='TVF19TV',
        country='France',
        velocity=224.22,
        height=10942.32
    )

@pytest.fixture
def aircraft2():
    return Aircraft(
        id_board='ab6fdd',
        callsign='AAL960',
        country='United States',
        velocity=60.39,
        height=739.14
    )


@pytest.fixture
def aircraft3():
    return Aircraft(
        id_board='a3feee',
        callsign='N357BG',
        country='Ireland',
        velocity=341.81,
        height=12184.38
    )