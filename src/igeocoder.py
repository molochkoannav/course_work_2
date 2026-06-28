from src.base_igeocoder import BaseIGeocoder
from requests import get, RequestException
import json
from pathlib import Path
import logging

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_geocode = log_dir / "igeocoder.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
logger_geocode = logging.getLogger("igeocoder")
logger_geocode.setLevel(logging.DEBUG)


file_handler_geocode = logging.FileHandler(log_geocode, mode="w", encoding="utf-8")
file_handler_geocode.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_geocode.setFormatter(formatter)


logger_geocode.addHandler(file_handler_geocode)
logger_geocode.propagate = False

class IGeocoder(BaseIGeocoder):
    """Класс для отработки геокодирования по стране """
    name_country: str

    def __init__(self, name_country):
        logger_geocode.info(f"Создан объект класса IGeocoder с именем {name_country}")
        self.name_country = name_country
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'

    def get_bounding_box(self):
        """Метод для получения координат"""
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        params_nominatim = {
            'country': self.name_country,
            'format': 'json',
            'limit': 1,
        }
        try:
            logger_geocode.info("Отправлен запрос на сервер")
            response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
            logger_geocode.info(f"Получен ответ от сервера {response.status_code}")
            data = response.json()

            if data:  # Проверяем, что данные получены
                # Получаем bounding box
                geo_coordinates = data[0].get('boundingbox')

                # Возвращаем координаты в виде словаря
                return {
                    'south': float(geo_coordinates[0]),  # южная широта
                    'north': float(geo_coordinates[1]),  # северная широта
                    'west': float(geo_coordinates[2]),  # западная долгота
                    'east': float(geo_coordinates[3]),  # восточная долгота
                    'lat': float(data[0].get('lat')),
                    'lon': float(data[0].get('lon')),
                }
            else:
                logger_geocode.error(f"Не удалось получить bounding box для страны {self.name_country}")
                return None

        except RequestException as e:
            logger_geocode.error(f"Ошибка при выполнении запроса к API: {e}")
            return None

        except json.JSONDecodeError as e:
            logger_geocode.error(f"Ошибка парсинга JSON ответа: {e}")
            return None

        except (KeyError, IndexError, TypeError, ValueError) as e:
            logger_geocode.error(f"Ошибка обработки данных для страны {self.name_country}: {e}")
            return None

        except Exception as e:
            logger_geocode.error(f"Непредвиденная ошибка: {e}", exc_info=True)
            return None