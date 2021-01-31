from abc import ABC, abstractmethod
from typing import Iterable

from .distance_matrix import LazyAerialDistanceMatrix
from .models import Cargo, Route, Truck


class MinimalRouteSolver(ABC):
    def __init__(self, cargos: Iterable[Cargo], trucks: Iterable[Truck]):
        self.cargos = cargos
        self.trucks = trucks

    @abstractmethod
    def solve(self) -> list[Route]:
        pass


class SolverByShortestOverallRoute(MinimalRouteSolver):
    def calculate_distance_matrix(self):
        self.distance_matrix = LazyAerialDistanceMatrix()

    def generate_sorted_shortest_routes_by_cargo(self, cargo: Cargo) -> list[Route]:
        routes = []
        for truck in self.trucks:
            distance = self.distance_matrix.distance(
                truck.location, cargo.origin_location
            ) + self.distance_matrix.distance(
                cargo.origin_location, cargo.destination_location
            )
            routes.append(Route(truck, cargo, distance))

        routes.sort(key=lambda r: r.distance)
        return routes

    def find_shortest_route(
        self, routes_by_cargo: dict[Cargo, Iterable[Route]], busy_trucks: set[Truck]
    ) -> Route:
        shortest_route_by_cargo = {}
        for cargo_routes in routes_by_cargo.values():
            for index, route in enumerate(cargo_routes):
                if route.truck in busy_trucks:
                    cargo_routes.pop(index)
                else:
                    shortest_route_by_cargo[route.cargo] = route
                    break

        return min(shortest_route_by_cargo.values(), key=lambda r: r.distance)

    def solve(self) -> list[Route]:
        self.calculate_distance_matrix()
        routes_by_cargo = {
            cargo: self.generate_sorted_shortest_routes_by_cargo(cargo)
            for cargo in self.cargos
        }

        solution = {}
        for _ in range(len(self.cargos)):
            shortest_route = self.find_shortest_route(routes_by_cargo, solution.keys())
            solution[shortest_route.truck] = shortest_route
            del routes_by_cargo[shortest_route.cargo]

        return list(solution.values())
