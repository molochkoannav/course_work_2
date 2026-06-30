from pathlib import Path
import logging

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_aircraft_info = log_dir / "aircraft_info.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
log_air_info = logging.getLogger("aircraft_info")
log_air_info.setLevel(logging.DEBUG)


file_handler_aircraft_info = logging.FileHandler(log_aircraft_info, mode="w", encoding="utf-8")
file_handler_aircraft_info.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_aircraft_info.setFormatter(formatter)


log_air_info.addHandler(file_handler_aircraft_info)
log_air_info.propagate = False

class Aircraft():
    """Класс для работы с данными о самолетах"""

    id_board: str
    callsign: str
    country: str
    velocity: float
    height: float
    def __init__(self, id_board: str, callsign: str, country: str, velocity: float, height: float):
        self.id_board_valid(id_board)
        self.callsign_valid(callsign)
        self.country_valid(country)
        self.velocity_valid(velocity)
        self.height_valid(height)

        self.id_board = id_board
        self.callsign = callsign
        self.country = country
        self.velocity = velocity if velocity is not None else 0.0
        self.height = height if height is not None else 0

    @staticmethod
    def id_board_valid(id_board: str) -> None:
        """Валидация бортового номера"""
        if not isinstance(id_board, str) or not id_board.strip():
            raise ValueError("ID борта должен быть непустой строкой")

    @staticmethod
    def callsign_valid(callsign: str) -> None:
        """Валидация callsign"""
        if not isinstance(callsign, str) or not callsign.strip():
            raise ValueError("Callsign должен быть непустой строкой")

    @staticmethod
    def country_valid(country: str) -> None:
        """Валидация страны"""
        if not isinstance(country, str) or not country.strip():
            raise ValueError("Страна должна быть непустой строкой")

    @staticmethod
    def velocity_valid(velocity: float) -> None:
        """Валидация скорости"""
        if not isinstance(velocity, (int, float)):
            raise ValueError("Скорость должна быть числом")

    @staticmethod
    def height_valid(height: float) -> None:
        """Валидация высоты"""
        if height is not None:
            if not isinstance(height, (int, float)):
                raise TypeError("Высота должна быть числом или None")
            if height < 0:
                raise ValueError("Высота не может быть отрицательной")


    @classmethod
    def state_converting(cls,state):
        """Создает объект Aircraft из сырых данных OpenSky"""
        try:
            log_air_info.info(f"Создается объект Aircraft из данных: state")
            return cls( id_board=state[0],
                        callsign=state[1].strip() if state[1] else "UNKNOWN",
                        country=state[2] or "UNKNOWN",
                        velocity=float(state[9]) if state[9] is not None else 0.0,
                        height=float(state[13]) if state[13] is not None else None
                        )
        except (IndexError, ValueError, TypeError) as e:
            log_air_info.error(f"Ошибка при конвертации данных: {e}")
            return None

    def __lt__(self, other):
        """Сравнение по скорости"""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.velocity < other.velocity

    def __gt__(self, other):
        """Сравнение по высоте"""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.height > other.height

    def __eq__(self, other):
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.id_board == other.id_board

    def __str__(self):
        return f"Борт {self.id_board} c позывным {self.callsign}, принадлежащий {self.country}, движется с {self.velocity} м/с, на высоте {self.height} м"



