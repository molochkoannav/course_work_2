import json

from src.base_aircraft_storage import BaseAircraftStorage


class AircraftStorageJSON(BaseAircraftStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []

    def load(self):
        try:
            with open(self.file_path, "r", encoding="UTF-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.data = data
                    return self.data
                else:
                    self.data = [data] if data else []
                    return self.data
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка при чтении файла: {e}"

    def save(self, data):
        try:
            with open(self.file_path, 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return "Данные успешно сохранены"
        except Exception as e:
            return f"При сохранении возникла неизвестная ошибка: {e}"

    def connect(self):
        pass

    def disconnect(self):
        pass

    def add_aircraft(self, aircraft: dict):
        try:
            try:
                with open(self.file_path, 'r', encoding='UTF-8') as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data] if existing_data else []
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []

            for existing in existing_data:
                if existing.get('id_board') == aircraft.get('id_board'):
                    return f"Самолёт с бортовым номером {aircraft.get('id_board')} уже существует"

            existing_data.append(aircraft)

            with open(self.file_path, 'w', encoding='UTF-8') as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)

            self.data = existing_data
            return f"Самолёт успешно добавлен. Всего: {len(existing_data)}"

        except Exception as e:
            return f"Ошибка при добавлении самолёта: {e}"

    def remove_aircraft(self, aircraft_id: str):
        try:
            try:
                with open(self.file_path, 'r', encoding='UTF-8') as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data] if existing_data else []
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []

            initial_count = len(existing_data)
            existing_data = [aircraft for aircraft in existing_data
                             if aircraft.get('id_board') != aircraft_id]

            if len(existing_data) == initial_count:
                return f"Самолёт с бортовым номером {aircraft_id} не найден"

            with open(self.file_path, 'w', encoding='UTF-8') as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)

            self.data = existing_data
            return f"Самолёт успешно удален. Всего: {len(existing_data)}"

        except Exception as e:
            return f"Ошибка при удалении самолёта: {e}"

    def search_aircrafts(self, search_params: dict):
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data] if existing_data else []

            filtered_data = []
            for aircraft in existing_data:
                matches = True
                for key, value in search_params.items():
                    if key not in aircraft or aircraft[key] != value:
                        matches = False
                        break
                if matches:
                    filtered_data.append(aircraft)

            return filtered_data if filtered_data else []

        except FileNotFoundError:
            return []
        except Exception as e:
            return []