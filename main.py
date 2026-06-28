from src.igeocoder import IGeocoder
if __name__ == '__main__':
    country1 = IGeocoder("Россия")
    print(country1.get_bounding_box())

