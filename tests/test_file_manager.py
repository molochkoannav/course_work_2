def test_initialization(storage, temp_file):
    """Тест инициализации хранилища."""
    assert storage.data == []
    assert storage.file_path == temp_file
    assert storage.file_manager is not None
    assert storage.serializer is not None
    assert storage.validator is not None


def test_add_aircraft_valid(storage, aircraft1):
    """Тест добавления валидного самолета."""
    aircraft_dict = {
        "id_board": aircraft1.id_board,
        "callsign": aircraft1.callsign,
        "country": aircraft1.country,
        "velocity": aircraft1.velocity,
        "height": aircraft1.height,
    }
    result = storage.add_aircraft(aircraft_dict)
    assert "Самолёт успешно добавлен" in result
    assert len(storage.data) == 1
    assert storage.data[0]["id_board"] == "39de4f"
    assert storage.data[0]["callsign"] == "TVF19TV"
    assert storage.data[0]["country"] == "France"
    assert storage.data[0]["velocity"] == 224.22
    assert storage.data[0]["height"] == 10942.32


def test_add_multiple_aircrafts(storage, aircraft1, aircraft2, aircraft3):
    """Тест добавления нескольких самолетов."""
    storage.add_aircraft(
        {
            "id_board": aircraft1.id_board,
            "callsign": aircraft1.callsign,
            "country": aircraft1.country,
            "velocity": aircraft1.velocity,
            "height": aircraft1.height,
        }
    )
    storage.add_aircraft(
        {
            "id_board": aircraft2.id_board,
            "callsign": aircraft2.callsign,
            "country": aircraft2.country,
            "velocity": aircraft2.velocity,
            "height": aircraft2.height,
        }
    )
    storage.add_aircraft(
        {
            "id_board": aircraft3.id_board,
            "callsign": aircraft3.callsign,
            "country": aircraft3.country,
            "velocity": aircraft3.velocity,
            "height": aircraft3.height,
        }
    )

    assert len(storage.data) == 3
    assert storage.data[0]["id_board"] == "39de4f"
    assert storage.data[1]["id_board"] == "ab6fdd"
    assert storage.data[2]["id_board"] == "a3feee"


def test_add_aircraft_invalid(storage):
    """Тест добавления невалидного самолета (отсутствуют обязательные поля)."""
    invalid_aircraft = {"callsign": "INVALID", "country": "Test", "velocity": 100.00, "height": 5000.00}
    result = storage.add_aircraft(invalid_aircraft)
    assert "Ошибка: отсутствуют обязательные поля" in result
    assert len(storage.data) == 0


def test_add_duplicate_aircraft(storage, aircraft1):
    """Тест добавления дублирующего самолета."""
    aircraft_dict = {
        "id_board": aircraft1.id_board,
        "callsign": aircraft1.callsign,
        "country": aircraft1.country,
        "velocity": aircraft1.velocity,
        "height": aircraft1.height,
    }
    storage.add_aircraft(aircraft_dict)
    result = storage.add_aircraft(aircraft_dict)
    assert "уже существует" in result
    assert len(storage.data) == 1


def test_remove_aircraft_existing(storage, aircraft1, aircraft2, aircraft3):
    """Тест удаления существующего самолета."""
    storage.add_aircraft(
        {
            "id_board": aircraft1.id_board,
            "callsign": aircraft1.callsign,
            "country": aircraft1.country,
            "velocity": aircraft1.velocity,
            "height": aircraft1.height,
        }
    )
    storage.add_aircraft(
        {
            "id_board": aircraft2.id_board,
            "callsign": aircraft2.callsign,
            "country": aircraft2.country,
            "velocity": aircraft2.velocity,
            "height": aircraft2.height,
        }
    )
    storage.add_aircraft(
        {
            "id_board": aircraft3.id_board,
            "callsign": aircraft3.callsign,
            "country": aircraft3.country,
            "velocity": aircraft3.velocity,
            "height": aircraft3.height,
        }
    )
    assert len(storage.data) == 3

    result = storage.remove_aircraft("ab6fdd")
    assert "Самолёт успешно удален" in result
    assert len(storage.data) == 2

    ids = [aircraft["id_board"] for aircraft in storage.data]
    assert "39de4f" in ids
    assert "ab6fdd" not in ids
    assert "a3feee" in ids
