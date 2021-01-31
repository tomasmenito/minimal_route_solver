from typing import NamedTuple


class Location(NamedTuple):
    city: str
    state: str
    lat: float
    lng: float


class Cargo(NamedTuple):
    product: str
    origin_location: Location
    destination_location: Location


class Truck(NamedTuple):
    truck: str
    location: Location


class Route(NamedTuple):
    truck: Truck
    cargo: Cargo
    distance: float
