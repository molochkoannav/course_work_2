import json
import logging
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_serializer = log_dir / "storage.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
log_air_serializer = logging.getLogger("serializer")
log_air_serializer.setLevel(logging.DEBUG)

file_handler_serializer = logging.FileHandler(log_serializer, mode="w", encoding="utf-8")
file_handler_serializer.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_serializer.setFormatter(formatter)

log_air_serializer.addHandler(file_handler_serializer)
log_air_serializer.propagate = False


class JSONSerializer:
    """Отвечает за преобразование данных в JSON и обратно."""

    @staticmethod
    def serialize(data: List[Dict[str, Any]]) -> str:
        """Преобразует список словарей в JSON-строку."""
        return json.dumps(data, indent=4, ensure_ascii=False)

    @staticmethod
    def deserialize(json_str: str) -> List[Dict[str, Any]]:
        """Преобразует JSON-строку в список словарей."""
        try:
            log_air_serializer.info("Преобразование файла")
            data = json.loads(json_str)
            if isinstance(data, list):
                log_air_serializer.info("Файл преобразован")
                return data
            return [data] if data else []
        except json.JSONDecodeError:
            log_air_serializer.error("Ошибка преобразования файла")
            return []

    @staticmethod
    def load_from_file(file_path: str) -> List[Dict[str, Any]]:
        """Загружает и парсит JSON из файла."""
        try:
            log_air_serializer.info(f"Попытка открыть файл по пути {file_path}")
            with open(file_path, "r", encoding="UTF-8") as f:
                return JSONSerializer.deserialize(f.read())
        except FileNotFoundError:
            log_air_serializer.error("Файл не найден")
            return []
        except Exception as e:
            log_air_serializer.error(f"Ошибка при открытии файла: {e}")
            return []

    @staticmethod
    def save_to_file(file_path: str, data: List[Dict[str, Any]]) -> bool:
        """Сохраняет данные в JSON-файл."""
        try:
            log_air_serializer.info(f"Сохранение файла по пути {file_path}")
            with open(file_path, "w", encoding="UTF-8") as f:
                f.write(JSONSerializer.serialize(data))
            return True
        except Exception as e:
            log_air_serializer.error(f"Ошибка при сохранении файла: {e}")
            return False
