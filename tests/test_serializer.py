import json

from src.serializer import JSONSerializer


def test_serialize_aircraft_data():
    """Тест сериализации данных самолета."""
    data = [{"id_board": "4cc278", "callsign": "ICE8K", "country": "Iceland", "velocity": 259.73, "height": 12298.68}]

    result = JSONSerializer.serialize(data)

    assert isinstance(result, str), "Результат должен быть строкой"
    assert "4cc278" in result, "ID должен присутствовать"
    assert "ICE8K" in result, "Позывной должен присутствовать"
    assert "Iceland" in result, "Страна должна присутствовать"
    assert "259.73" in result, "Скорость должна присутствовать"
    assert "12298.68" in result, "Высота должна присутствовать"

    parsed = json.loads(result)
    assert parsed == data, "Данные должны корректно сериализоваться"


def test_deserialize_aircraft_data():
    """Тест десериализации данных самолета."""
    json_str = """[{
        "id_board": "4cc278",
        "callsign": "ICE8K",
        "country": "Iceland",
        "velocity": 259.73,
        "height": 12298.68
    }]"""

    result = JSONSerializer.deserialize(json_str)

    assert isinstance(result, list), "Результат должен быть списком"
    assert len(result) == 1, "Должен быть 1 элемент"
    assert result[0]["id_board"] == "4cc278", "ID должен совпадать"
    assert result[0]["callsign"] == "ICE8K", "Позывной должен совпадать"
    assert result[0]["country"] == "Iceland", "Страна должна совпадать"
    assert result[0]["velocity"] == 259.73, "Скорость должна совпадать"
    assert result[0]["height"] == 12298.68, "Высота должна совпадать"


def test_serialize_multiple_aircraft():
    """Тест сериализации нескольких самолетов."""
    data = [
        {"id_board": "4cc278", "callsign": "ICE8K", "country": "Iceland", "velocity": 259.73, "height": 12298.68},
        {"id_board": "4ca41e", "callsign": "HAWKEYE", "country": "Ireland", "velocity": 72.51, "height": 1600.2},
    ]

    result = JSONSerializer.serialize(data)

    assert "4cc278" in result, "Первый ID должен присутствовать"
    assert "4ca41e" in result, "Второй ID должен присутствовать"
    assert "ICE8K" in result, "Первый позывной должен присутствовать"
    assert "HAWKEYE" in result, "Второй позывной должен присутствовать"

    parsed = json.loads(result)
    assert len(parsed) == 2, "Должно быть 2 элемента"
    assert parsed == data, "Данные должны корректно сериализоваться"
