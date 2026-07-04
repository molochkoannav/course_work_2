from typing import Any
from typing import Dict
from typing import List


class AircraftValidator:
    """Отвечает за валидацию данных о самолётах."""

    @staticmethod
    def is_duplicate(existing_data: List[Dict[str, Any]], aircraft: Dict[str, Any]) -> bool:
        """Проверяет, существует ли самолёт с таким же id_board."""
        board_id = aircraft.get("id_board")
        if board_id is None:
            return False

        for existing in existing_data:
            if existing.get("id_board") == board_id:
                return True
        return False

    @staticmethod
    def validate_aircraft(aircraft: Dict[str, Any]) -> bool:
        """Проверяет, что самолёт содержит обязательные поля."""
        required_fields = ["id_board", "callsign", "country", "velocity", "height"]
        return all(field in aircraft for field in required_fields)

    @staticmethod
    def filter_by_criteria(data: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Фильтрует данные по заданным критериям (точное совпадение)."""
        if not criteria:
            return data

        result = []
        for item in data:
            matches = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    matches = False
                    break
            if matches:
                result.append(item)
        return result
