import json
from unittest.mock import patch, Mock
from pathlib import Path
import sys

# Добавляем путь к вашему модулю
sys.path.append(str(Path(__file__).parent.parent))

from src.geocoder import Geocoder


def test_geocoder_init():
    """Тест инициализации"""
    geocoder = Geocoder("Russia")
    assert geocoder.name_country == "Russia"
    assert geocoder.openstreetmap_url == 'https://nominatim.openstreetmap.org/search'


def test_get_bounding_box_success():
    """Тест успешного получения данных"""
    geocoder = Geocoder("Russia")

    with patch('src.geocoder.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'boundingbox': ['55.0', '60.0', '30.0', '40.0'],
                'lat': '57.5',
                'lon': '35.0'
            }
        ]
        mock_get.return_value = mock_response

        result = geocoder.get_bounding_box()

        assert result is not None
        assert isinstance(result, dict)
        assert result['south'] == 55.0
        assert result['north'] == 60.0
        assert result['west'] == 30.0
        assert result['east'] == 40.0
        assert result['lat'] == 57.5
        assert result['lon'] == 35.0
        assert all(isinstance(v, float) for v in result.values())


def test_get_bounding_box_empty_response():
    """Тест пустого ответа"""
    geocoder = Geocoder("Russia")

    with patch('src.geocoder.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = geocoder.get_bounding_box()

        assert result is None


def test_get_bounding_box_request_exception():
    """Тест ошибки запроса"""
    geocoder = Geocoder("Russia")

    with patch('src.geocoder.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")

        result = geocoder.get_bounding_box()

        assert result is None


def test_get_bounding_box_json_error():
    """Тест ошибки в получении JSON ответа"""
    geocoder = Geocoder("Russia")

    with patch('src.geocoder.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response

        result = geocoder.get_bounding_box()

        assert result is None


def test_get_bounding_box_missing_boundingbox():
    """Тест отсутствия ключа boundingbox"""
    geocoder = Geocoder("Russia")

    with patch('src.geocoder.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'lat': '57.5', 'lon': '35.0'}]
        mock_get.return_value = mock_response

        result = geocoder.get_bounding_box()

        assert result is None
