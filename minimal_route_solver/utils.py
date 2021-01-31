from haversine import Unit, haversine

from .models import Location


def calculate_haversine_distance(first: Location, second: Location):
    return haversine((first.lat, first.lng), (second.lat, second.lng), unit=Unit.MILES)
