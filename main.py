from src.aircraft import Aircraft
from src.geocoder import Geocoder
from src.aircraft_sourse import AircraftSourse
from src.aircraft_storage import AircraftStorageJSON


if __name__ == '__main__':
    geocoder = Geocoder('Ireland')
    bounding_box = geocoder.get_bounding_box()
    aircraft_source = AircraftSourse(bounding_box)
    states = aircraft_source.get_aeroplanes()
    print(states)
    aircraft_list = [Aircraft.state_converting(state) for state in states]
    if states:
        print(f"Найдено {len(states)} самолетов над {geocoder.name_country}")

    aircraft_dict = [obj.__dict__ for obj in aircraft_list]
    storage = AircraftStorageJSON("data/aircraft_dict_1.json")
    storage.data = aircraft_dict
    storage.save()
    search_params = {"callsign": "DAL4"}
    result = storage.search_aircrafts(search_params)
    print(result)








