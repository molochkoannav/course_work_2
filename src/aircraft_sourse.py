from src.base_iaircraft_sourse import BaseIAircraftSourse
from requests import get, RequestException
import json
from pathlib import Path
import logging

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_aircraft= log_dir / "iaircraft.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
logger_aircraft = logging.getLogger("iaircraft")
logger_aircraft.setLevel(logging.DEBUG)


file_handler_aircraft = logging.FileHandler(log_aircraft, mode="w", encoding="utf-8")
file_handler_aircraft.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_aircraft.setFormatter(formatter)


logger_aircraft.addHandler(file_handler_aircraft)
logger_aircraft.propagate = False

class AircraftSourse(BaseIAircraftSourse):
    """Класс для отработки получения данных о самолетах"""

    def __init__(self, bounding_box=None):
        self.opensky_url = 'https://opensky-network.org/api/states/all?'
        self.bounding_box = bounding_box
        self.aeroplanes = None
        logger_aircraft.info(f"Создан объект AircraftSource с bounding_box: {bounding_box}")

    def get_aeroplanes(self, bounding_box=None):
        """Получение списка самолетов"""
        bbox = bounding_box if bounding_box is not None else self.bounding_box
        if not bbox:
            logger_aircraft.error("Не указаны координаты для поиска самолетов")
            return None
        params = {
            'lamin': bbox['south'],
            'lamax': bbox['north'],
            'lomin': bbox['west'],
            'lomax': bbox['east'],
        }
        try:
            logger_aircraft.info(f"Отправлен запрос к OpenSky с параметрами: {params}")
            response = get(url=self.opensky_url, params=params)

            if response.status_code != 200:
                logger_aircraft.error(f"Ошибка запроса к OpenSky: {response.status_code}")
                return None

            self.aeroplanes = response.json()
            states = self.aeroplanes.get('states', [])
            logger_aircraft.info(f"Получено {len(states)} самолетов")

            return states

        except RequestException as e:
            logger_aircraft.error(f"Ошибка при запросе к OpenSky: {e}")
            return None
        except json.JSONDecodeError as e:
            logger_aircraft.error(f"Ошибка парсинга ответа OpenSky: {e}")
            return None
        except Exception as e:
            logger_aircraft.error(f"Непредвиденная ошибка: {e}", exc_info=True)
            return None
