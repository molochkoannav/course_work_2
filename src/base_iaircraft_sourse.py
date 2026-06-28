from abc import ABC, abstractmethod
class BaseIAircraftSource(ABC):
    """Базовый класс для определения положения самолетов"""
    @abstractmethod
    def get_states(self, bbox: tuple) -> list:
        pass
