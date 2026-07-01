import json
from typing import Any, Dict, List


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
            data = json.loads(json_str)
            if isinstance(data, list):
                return data
            return [data] if data else []
        except json.JSONDecodeError:
            return []

    @staticmethod
    def load_from_file(file_path: str) -> List[Dict[str, Any]]:
        """Загружает и парсит JSON из файла."""
        try:
            with open(file_path, 'r', encoding='UTF-8') as f:
                return JSONSerializer.deserialize(f.read())
        except FileNotFoundError:
            return []
        except Exception:
            return []

    @staticmethod
    def save_to_file(file_path: str, data: List[Dict[str, Any]]) -> bool:
        """Сохраняет данные в JSON-файл."""
        try:
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(JSONSerializer.serialize(data))
            return True
        except Exception:
            return False