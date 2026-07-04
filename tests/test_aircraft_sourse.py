import unittest
from unittest.mock import patch, Mock
import json
from pathlib import Path
from src.base_iaircraft_sourse import BaseIAircraftSourse
from src.aircraft_sourse import AircraftSourse

class TestAircraftSourse(unittest.TestCase):
    """Тесты для класса AircraftSourse"""

    def setUp(self):
        """Подготовка к тестам"""
        self.bbox = {
            'south': 55.0,
            'north': 56.0,
            'west': 37.0,
            'east': 38.0
        }
        self.aircraft_source = AircraftSourse(bounding_box=self.bbox)

    def test_init(self):
        """Тест инициализации объекта"""
        self.assertEqual(self.aircraft_source.opensky_url, 'https://opensky-network.org/api/states/all?')
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

    @patch('src.aircraft_sourse.get')
    def test_get_aeroplanes_success(self, mock_get):
        """Тест успешного получения списка самолетов"""
        # Подготовка мок-ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'states': [
                ['abc123', 'Boeing 737', 'USA', 12345, 12345.6, 12345.7, 10000, True],
                ['def456', 'Airbus A320', 'Germany', 54321, 54321.6, 54321.7, 8000, False]
            ]
        }
        mock_get.return_value = mock_response
