import pytest

from src.aircraft import Aircraft

def test_max_velocity(aircraft1, aircraft2, aircraft3):
    max_velocity = max([aircraft1, aircraft2, aircraft3], key=lambda x: x.velocity)
    assert max_velocity == aircraft3

def test_min_height(aircraft1, aircraft2, aircraft3):
    min_height = min([aircraft1, aircraft2, aircraft3], key=lambda x: x.height)
    assert min_height == aircraft2

def test_str(aircraft1):
    assert str(aircraft1) == "Борт 39de4f c позывным TVF19TV, принадлежащий France, движется с 224.22 м/с, на высоте 10942.32 м"


def test_id_board_valid():
    """Тест валидации бортового номера"""
    Aircraft.id_board_valid("ABC123")
    with pytest.raises(ValueError, match="ID борта должен быть непустой строкой"):
        Aircraft.id_board_valid("")
    with pytest.raises(ValueError, match="ID борта должен быть непустой строкой"):
        Aircraft.id_board_valid(123)
    with pytest.raises(ValueError, match="ID борта должен быть непустой строкой"):
        Aircraft.id_board_valid(None)


def test_callsign_valid():
    """Тест валидации callsign"""
    Aircraft.callsign_valid("CSN123")
    with pytest.raises(ValueError, match="Callsign должен быть непустой строкой"):
        Aircraft.callsign_valid("")
    with pytest.raises(ValueError, match="Callsign должен быть непустой строкой"):
        Aircraft.callsign_valid(123)
    with pytest.raises(ValueError, match="Callsign должен быть непустой строкой"):
        Aircraft.callsign_valid(None)


def test_country_valid():
    """Тест валидации страны"""
    Aircraft.country_valid("Russia")
    with pytest.raises(ValueError, match="Страна должна быть непустой строкой"):
        Aircraft.country_valid("")
    with pytest.raises(ValueError, match="Страна должна быть непустой строкой"):
        Aircraft.country_valid(123)
    with pytest.raises(ValueError, match="Страна должна быть непустой строкой"):
        Aircraft.country_valid(None)

def test_velocity_valid():
    """Тест валидации скорости"""
    Aircraft.velocity_valid(900.5)
    Aircraft.velocity_valid(900)
    Aircraft.velocity_valid(0.0)
    Aircraft.velocity_valid(-100)
    with pytest.raises(ValueError, match="Скорость должна быть числом"):
        Aircraft.velocity_valid("900")
    with pytest.raises(ValueError, match="Скорость должна быть числом"):
        Aircraft.velocity_valid(None)
    with pytest.raises(ValueError, match="Скорость должна быть числом"):
        Aircraft.velocity_valid([900])

def test_height_valid():
    """Тест валидации высоты"""
    Aircraft.height_valid(11000.5)
    Aircraft.height_valid(11000)
    Aircraft.height_valid(0.0)
    Aircraft.height_valid(None)
    with pytest.raises(TypeError, match="Высота должна быть числом или None"):
        Aircraft.height_valid("11000")
    with pytest.raises(TypeError, match="Высота должна быть числом или None"):
        Aircraft.height_valid([11000])
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        Aircraft.height_valid(-100)
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        Aircraft.height_valid(-0.1)


def test_state_converting_success():
    """Тест успешного создания объекта из данных OpenSky"""

    state_data = [
        "ABC123",  # id_board
        "CSN123",  # callsign
        "Russia",  # country
        None,  # time_position
        None,  # last_contact
        None,  # longitude
        None,  # latitude
        None,  # baro_altitude
        None,  # on_ground
        900.5,  # velocity
        None,  # true_track
        None,  # vertical_rate
        None,  # sensors
        11000.0,  # altitude
        None,  # geo_altitude
        None,  # squawk
        None,  # spi
        None  # position_source
    ]

    aircraft = Aircraft.state_converting(state_data)
    assert aircraft is not None
    assert aircraft.id_board == "ABC123"
    assert aircraft.callsign == "CSN123"
    assert aircraft.country == "Russia"
    assert aircraft.velocity == 900.5
    assert aircraft.height == 11000.0