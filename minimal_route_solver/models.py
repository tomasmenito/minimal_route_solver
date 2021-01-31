from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    city: str
    state: str
    lat: float
    lng: float


@dataclass(frozen=True)
class Cargo:
    product: str
    origin_location: Location
    destination_location: Location


@dataclass(frozen=True)
class Truck:
    truck: str
    location: Location


@dataclass(frozen=True)
class Route:
    truck: Truck
    cargo: Cargo
    distance: float
