from abc import ABC, abstractmethod
from collections import defaultdict

from .models import Location
from .utils import calculate_haversine_distance


class DistanceMatrix(ABC):
    @abstractmethod
    def distance(self, origin: Location, destination: Location) -> float:
        pass


class LazyAerialDistanceMatrix(DistanceMatrix):
    distances: defaultdict[Location, dict[Location, float]] = defaultdict(dict)

    def distance(self, origin: Location, destination: Location) -> float:
        first, second = min(origin, destination), max(origin, destination)
        if self.distances[first].get(second) is None:
            self.distances[first][second] = calculate_haversine_distance(first, second)

        return self.distances[first][second]
