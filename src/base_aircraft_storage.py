
from abc import ABC, abstractmethod

class BaseAircraftStorage(ABC):
    """Абстрактный класс для хранения, получения, добавления, удаления данных о самолетах"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._next_id = 1
        self.load()

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def add_aircraft(self, aircraft: dict):
        pass

    @abstractmethod
    def remove_aircraft(self, aircraft_id: str):
        pass

    @abstractmethod
    def search_aircrafts(self, search_params: dict):
        pass
