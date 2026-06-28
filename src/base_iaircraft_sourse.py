from abc import ABC, abstractmethod
class BaseIAircraftSourse(ABC):
    """Базовый класс для определения положения самолетов"""
    @abstractmethod
    def get_aeroplanes(self, bbox: tuple) -> list:
        pass
