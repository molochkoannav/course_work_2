from abc import ABC, abstractmethod

class BaseIGeocoder(ABC):
    """Базовый класс для создания запроса по стране"""
    @abstractmethod
    def get_bounding_box(self):
        pass


