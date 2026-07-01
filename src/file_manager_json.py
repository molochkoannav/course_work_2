
import json
from pathlib import Path
from typing import Any, List, Dict
import logging


current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "file_manager.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
log_file_manager = logging.getLogger("file_manager")
log_file_manager.setLevel(logging.DEBUG)


file_handler_file_manager = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler_file_manager.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_file_manager.setFormatter(formatter)


log_file_manager.addHandler(file_handler_file_manager)
log_file_manager.propagate = False


class FileManager:
    """Отвечает за чтение и запись данных в файл."""

    def __init__(self, file_path: str, logger: logging.Logger = None):
        self.file_path = Path(file_path)


    def read(self) -> List[Dict[str, Any]]:
        """Читает данные из файла. Возвращает список словарей."""
        try:
            log_file_manager.info("Чтение файла")
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    log_file_manager.info("Данные загружены")
                    return data
                elif data:
                    log_file_manager.info("Данные не являются списком")
                    return [data]
                return []
        except FileNotFoundError:
            log_file_manager.error("Файл не найден")
            return []
        except json.JSONDecodeError as e:
            log_file_manager.error(f"Ошибка парсинга JSON: {e}")
            return []
        except Exception as e:
            log_file_manager.error(f"Ошибка при чтении файла: {e}")
            return []

    def write(self, data: List[Dict[str, Any]]) -> bool:
        """Записывает данные в файл. Возвращает True при успехе."""
        try:
            log_file_manager.info("Пробуем записать файл")
            with open(self.file_path, 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                log_file_manager.info("данные загружены")
            return True
        except Exception as e:
            log_file_manager.error(f"Ошибка при записи файла: {e}")
            return False

    def exists(self) -> bool:
        """Проверяет существование файла."""
        return self.file_path.exists()