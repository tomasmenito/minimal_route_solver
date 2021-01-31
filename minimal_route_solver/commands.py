import csv
from operator import itemgetter

import click

from .models import Cargo, Location, Truck
from .solvers import SolverByShortestOverallRoute


def row_to_cargo(**data) -> Cargo:
    origin_location = Location(
        city=data.pop("origin_city"),
        state=data.pop("origin_state"),
        lat=float(data.pop("origin_lat")),
        lng=float(data.pop("origin_lng")),
    )

    destination_location = Location(
        city=data.pop("destination_city"),
        state=data.pop("destination_state"),
        lat=float(data.pop("destination_lat")),
        lng=float(data.pop("destination_lng")),
    )

    return Cargo(
        **data,
        origin_location=origin_location,
        destination_location=destination_location,
    )


def row_to_truck(**data) -> Truck:
    location = Location(
        city=data.pop("city"),
        state=data.pop("state"),
        lat=float(data.pop("lat")),
        lng=float(data.pop("lng")),
    )
    return Truck(**data, location=location)


@click.command()
@click.argument("cargo_file", required=True, type=click.File("r"))
@click.argument("truck_file", required=True, type=click.File("r"))
@click.argument("results_file", default="results.csv", type=click.File("w"))
def solve(cargo_file, truck_file, results_file):
    cargos_reader = csv.DictReader(cargo_file)
    trucks_reader = csv.DictReader(truck_file)

    cargos = [row_to_cargo(**row) for row in cargos_reader]
    trucks = [row_to_truck(**row) for row in trucks_reader]

    routes = SolverByShortestOverallRoute(cargos, trucks).solve()

    routes_data = [
        {
            "cargo": route.cargo.product,
            "truck": route.truck.truck,
            "distance": round(route.distance, 2),
        }
        for route in routes
    ]
    routes_data.sort(key=itemgetter("distance"))

    results_writer = csv.DictWriter(
        results_file, fieldnames=("cargo", "truck", "distance")
    )
    results_writer.writeheader()
    results_writer.writerows(routes_data)
