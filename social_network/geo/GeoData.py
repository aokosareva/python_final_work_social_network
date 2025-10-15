class GeoData:
    def __init__(self, address=None, lat=None, lon=None):
        self.__address = address
        self.__latitude = lat
        self.__longitude = lon

    def data(self) -> dict:
        return {
            'address': self.__address,
            'latitude': self.__latitude,
            'longitude': self.__longitude
        }
