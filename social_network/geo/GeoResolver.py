from geo.GeoData import GeoData
from geo.LocationIsUndefined import LocationIsUndefined


class GeoResolver:
    def __init__(self, geocoder):
        self.__geocoder = geocoder

    def load_by_location(self, location_query: str) -> GeoData:
        location = self.__geocoder.geocode(location_query)
        if location is None:
            raise LocationIsUndefined()
        return GeoData(location.address, location.latitude, location.longitude)

    def load_by_coords(self, lat, lon):
        coords_query = (lat, lon)
        location = self.__geocoder.reverse(coords_query)
        if location is None:
            raise LocationIsUndefined()
        return GeoData(location.address, location.latitude, location.longitude)
