from src.aircraft import Aircraft
from src.geocoder import Geocoder
from src.aircraft_sourse import AircraftSourse
from src.aircraft_storage import AircraftStorageJSON
if __name__ == '__main__':
    geocoder = Geocoder('Ireland')
    bounding_box = geocoder.get_bounding_box()
    aircraft_source = AircraftSourse(bounding_box)
    states = aircraft_source.get_aeroplanes()

    aircraft_list = []

    if states:
        print(f"Найдено {len(states)} самолетов над {geocoder.name_country}")


        for state in states:
            # print(state)
            aircraft = Aircraft.state_converting(state)
            if aircraft:
                aircraft_list.append(aircraft)
                aircraft_dict = [obj.__dict__ for obj in aircraft_list]
                json_saver = AircraftStorageJSON("data/aircraft_dict.json")
                json_saver.save(aircraft_dict)

                all_aircraft =
                print(all_aircraft)


        max_aircraft = max(aircraft_list, key=lambda x: x.velocity)
        min_height = min(aircraft_list, key=lambda a: a.height)
        print(f"{max_aircraft} \n {min_height}")







