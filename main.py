from src.geocoder import Geocoder
from src.aircraft_sourse import AircraftSourse
if __name__ == '__main__':
    geocoder = Geocoder('USA')
    bounding_box = geocoder.get_bounding_box()
    aircraft_source = AircraftSourse(bounding_box)
    states = aircraft_source.get_aeroplanes()

    if states:
        print(f"Найдено {len(states)} самолетов над {geocoder.name_country}")
    else:
        print("Самолеты не найдены или произошла ошибка")
else:
    print("Не удалось получить координаты страны")