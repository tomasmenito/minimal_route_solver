import csv
from operator import itemgetter

import click

from .models import Cargo, Location, Truck
from .solvers import SolverByMinimalOverallRoute

LOCATION_PROPS = {"city", "state", "lat", "lng"}


def _parse_cargo(data) -> Cargo:
    origin_location = Location(
        **{prop: data.pop(f"origin_{prop}") for prop in LOCATION_PROPS}
    )

    destination_location = Location(
        **{prop: data.pop(f"destination_{prop}") for prop in LOCATION_PROPS}
    )
    return Cargo(
        **data,
        origin_location=origin_location,
        destination_location=destination_location,
    )


def _parse_truck(data) -> Truck:
    location = Location(**{prop: data.pop(prop) for prop in LOCATION_PROPS})
    return Truck(**data, location=location)


@click.command()
@click.argument("cargo_file", required=True, type=click.File("r"))
@click.argument("truck_file", required=True, type=click.File("r"))
@click.argument("results_file", default="results.csv", type=click.File("w"))
def solve(cargo_file, truck_file, results_file):
    cargos_reader = csv.DictReader(cargo_file)
    trucks_reader = csv.DictReader(truck_file)

    cargos = [_parse_cargo(line) for line in cargos_reader]
    trucks = [_parse_truck(line) for line in trucks_reader]

    routes = SolverByMinimalOverallRoute(cargos, trucks).solve()

    routes_data = [
        {
            "cargo": route.cargo.product,
            "truck": route.truck.truck,
            "distance": route.distance,
        }
        for route in routes
    ]
    routes_data.sort(key=itemgetter("distance"))

    results_writer = csv.DictWriter(
        results_file, fieldnames=("cargo", "truck", "distance")
    )
    results_writer.writeheader()
    results_writer.writerows(routes_data)
