from src.base_aircraft_storage import BaseAircraftStorage
from src.file_manager_json import FileManager
from src.serializer import JSONSerializer
from src.validator import AircraftValidator
import logging
from pathlib import Path
from typing import Dict, Any, List

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)
log_storage = log_dir / "storage.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
log_air_storage = logging.getLogger("storage")
log_air_storage.setLevel(logging.DEBUG)

file_handler_storage = logging.FileHandler(log_storage, mode="w", encoding="utf-8")
file_handler_storage.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_storage.setFormatter(formatter)

log_air_storage.addHandler(file_handler_storage)
log_air_storage.propagate = False


class AircraftStorageJSON(BaseAircraftStorage):
    """Реализация хранилища для JSON-файлов с использованием композиции."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []
        self.file_manager = FileManager(file_path)
        self.serializer = JSONSerializer()
        self.validator = AircraftValidator()
        self.load()


    def load(self) -> List[Dict[str, Any]]:
        """Загружает данные из файла."""
        self.data = self.file_manager.read()
        log_air_storage.info(f"Загружено {len(self.data)} записей")
        return self.data

    def save(self) -> bool:
        """Сохраняет текущие данные в файл."""
        success = self.file_manager.write(self.data)
        if success:
            log_air_storage.info(f"Сохранено {len(self.data)} записей")
        return success


    def connect(self):
        """Заглушка для подключения к БД."""
        log_air_storage.debug("Метод connect() вызван (заглушка)")
        pass

    def disconnect(self):
        """Заглушка для отключения от БД."""
        log_air_storage.debug("Метод disconnect() вызван (заглушка)")
        pass

    def add_aircraft(self, aircraft: Dict[str, Any]) -> str:
        """Добавляет новый самолёт."""
        try:
            if not self.validator.validate_aircraft(aircraft):
                return "Ошибка: отсутствуют обязательные поля (id_board, model)"

            if self.validator.is_duplicate(self.data, aircraft):
                return f"Самолёт с бортовым номером {aircraft.get('id_board')} уже существует"

            self.data.append(aircraft)
            if self.save():
                log_air_storage.info(f"Добавлен самолёт {aircraft.get('id_board')}")
                return f"Самолёт успешно добавлен. Всего: {len(self.data)}"
            else:
                return "Ошибка при сохранении данных"

        except Exception as e:
            error_msg = f"Ошибка при добавлении самолёта: {e}"
            log_air_storage.error(error_msg)
            return error_msg

    def remove_aircraft(self, aircraft_id: str) -> str:
        """Удаляет самолёт по бортовому номеру."""
        try:
            initial_count = len(self.data)
            self.data = [aircraft for aircraft in self.data
                         if aircraft.get('id_board') != aircraft_id]

            if len(self.data) == initial_count:
                return f"Самолёт с бортовым номером {aircraft_id} не найден"

            if self.save():
                log_air_storage.info(f"Удалён самолёт {aircraft_id}")
                return f"Самолёт успешно удален. Всего: {len(self.data)}"
            else:
                return "Ошибка при сохранении данных"

        except Exception as e:
            error_msg = f"Ошибка при удалении самолёта: {e}"
            log_air_storage.error(error_msg)
            return error_msg

    def search_aircrafts(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Поиск самолётов по критериям."""
        try:
            clean_params = {}
            for key, value in search_params.items():
                if isinstance(value, str):
                    clean_params[key] = ' '.join(value.split())
                else:
                    clean_params[key] = value

            filtered = self.validator.filter_by_criteria(self.data, clean_params)
            log_air_storage.info(f"Найдено {len(filtered)} самолётов по критериям {clean_params}")
            return filtered

        except Exception as e:
            log_air_storage.error(f"Ошибка при поиске: {e}")
        return []


    def get_all(self) -> List[Dict[str, Any]]:
        """Возвращает все самолёты."""
        return self.data