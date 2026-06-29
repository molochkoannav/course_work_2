from src.aircraft import Aircraft
from src.geocoder import Geocoder
from src.aircraft_sourse import AircraftSourse
if __name__ == '__main__':
    geocoder = Geocoder('USA')
    bounding_box = geocoder.get_bounding_box()
    aircraft_source = AircraftSourse(bounding_box)
    states = aircraft_source.get_aeroplanes()

    aircraft_list = []

    if states:
        print(f"Найдено {len(states)} самолетов над {geocoder.name_country}")


        for state in states[:10]:
            # print(state)
            aircraft = Aircraft.state_converting(state)
            if aircraft:
                aircraft_list.append(aircraft)

        max_aircraft = max(aircraft_list, key=lambda x: x.velocity)
        min_height = min(aircraft_list, key=lambda a: a.height)
        print(f"{max_aircraft} \n {min_height}")





