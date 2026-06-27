from abc import ABC, abstractmethod

class BaseAeroplanesAPI(ABC):
    @abstractmethod
    def get_aeroplanes(self, name_country: str):
        pass