import json
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from src.aircraft_sourse import AircraftSourse


class TestAircraftSourse(unittest.TestCase):
    """Тесты для класса AircraftSourse"""

    def setUp(self):
        """Подготовка к тестам"""
        self.bbox = {"south": 55.0, "north": 56.0, "west": 37.0, "east": 38.0}
        self.aircraft_source = AircraftSourse(bounding_box=self.bbox)

    def test_init(self):
        """Тест инициализации объекта"""
        self.assertEqual(self.aircraft_source.opensky_url, "https://opensky-network.org/api/states/all?")
        self.assertEqual(self.aircraft_source.bounding_box, self.bbox)
        self.assertIsNone(self.aircraft_source.aeroplanes)

    def test_init_without_bounding_box(self):
        """Тест инициализации без bounding_box"""
        source = AircraftSourse()
        self.assertIsNone(source.bounding_box)

    def test_get_aeroplanes_without_bbox(self):
        """Тест получения самолетов без указания bounding_box"""
        source = AircraftSourse()
        result = source.get_aeroplanes()
        self.assertIsNone(result)

    @patch("src.aircraft_sourse.get")
    def test_get_aeroplanes_success(self, mock_get):
        """Тест успешного получения списка самолетов"""
        # Подготовка мок-ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "states": [
                ["abc123", "Boeing 737", "USA", 12345, 12345.6, 12345.7, 10000, True],
                ["def456", "Airbus A320", "Germany", 54321, 54321.6, 54321.7, 8000, False],
            ]
        }
        mock_get.return_value = mock_response

    @patch("src.aircraft_sourse.get")
    def test_get_aeroplanes_with_custom_bbox(self, mock_get):
        """Тест получения самолетов с кастомным bounding_box"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"states": []}
        mock_get.return_value = mock_response

        custom_bbox = {"south": 50.0, "north": 51.0, "west": 30.0, "east": 31.0}

        result = self.aircraft_source.get_aeroplanes(bounding_box=custom_bbox)
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]["params"]
        self.assertEqual(call_args["lamin"], custom_bbox["south"])
        self.assertEqual(call_args["lamax"], custom_bbox["north"])
        self.assertEqual(call_args["lomin"], custom_bbox["west"])
        self.assertEqual(call_args["lomax"], custom_bbox["east"])

    @patch("src.aircraft_sourse.get")
    def test_get_aeroplanes_error_status(self, mock_get):
        """Тест ошибки при получении самолетов (статус не 200)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = self.aircraft_source.get_aeroplanes()
        self.assertIsNone(result)

    @patch("src.aircraft_sourse.get")
    def test_get_aeroplanes_request_exception(self, mock_get):
        """Тест исключения RequestException"""
        mock_get.side_effect = Exception("Connection error")
        result = self.aircraft_source.get_aeroplanes()
        self.assertIsNone(result)

    @patch("src.aircraft_sourse.get")
    def test_get_aeroplanes_json_error(self, mock_get):
        """Тест ошибки парсинга JSON"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response

        result = self.aircraft_source.get_aeroplanes()

        self.assertIsNone(result)

    @patch("src.aircraft_sourse.get")
    def test_get_aeroplanes_no_states(self, mock_get):
        """Тест ответа без поля 'states'"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"other": "data"}
        mock_get.return_value = mock_response

        result = self.aircraft_source.get_aeroplanes()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)
