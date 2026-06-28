from src.igeocoder import IGeocoder
from src.iaircraft_source import IAircraftSource
if __name__ == '__main__':
    geocoder = IGeocoder('Russia')
    bounding_box = geocoder.get_bounding_box()
    aircraft_source = IAircraftSource(bounding_box)
    states = aircraft_source.get_states()

    if states:
        print(f"Найдено {len(states)} самолетов над Канадой")
    else:
        print("Самолеты не найдены или произошла ошибка")
else:
    print("Не удалось получить координаты страны")