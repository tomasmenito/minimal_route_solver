from abc import ABC, abstractmethod
from collections import defaultdict

from haversine import Unit, haversine

from .models import Location


class DistanceMatrix(ABC):
    @abstractmethod
    def distance(self, origin: Location, destination: Location) -> float:
        pass


class LazyAerialDistanceMatrix(DistanceMatrix):
    distances: defaultdict[Location, dict[Location, float]] = defaultdict(dict)

    def calculate_distance(self, first: Location, second: Location):
        return haversine(
            (first.lat, first.lng), (second.lat, second.lng), unit=Unit.MILES
        )

    def distance(self, origin: Location, destination: Location) -> float:
        first, second = min(origin, destination), max(origin, destination)
        if self.distances[first].get(second) is None:
            self.distances[first][second] = self.calculate_distance(first, second)

        return self.distances[first][second]
