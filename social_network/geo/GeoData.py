class GeoData:
    def __init__(self, value, lat=None, lon=None):
        self.__value = value
        self.__latitude = lat
        self.__longitude = lon

    def __str__(self):
        return self.__value

    def coords(self) -> dict:
        return {
            'latitude': self.__latitude,
            'longitude': self.__longitude
        }
