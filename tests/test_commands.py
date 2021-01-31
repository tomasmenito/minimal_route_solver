from io import StringIO
from unittest import mock

from click.testing import CliRunner

from minimal_route_solver.commands import (
    persist_results,
    row_to_cargo,
    row_to_truck,
    solve,
)
from tests.factories import CargoFactory, RouteFactory, TruckFactory


def test_row_to_cargo(cargo_csv_data):
    cargo = row_to_cargo(**cargo_csv_data)

    assert cargo.product == cargo_csv_data["product"]

    assert cargo.origin_location.city == cargo_csv_data["origin_city"]
    assert cargo.origin_location.state == cargo_csv_data["origin_state"]
    assert cargo.origin_location.lat == float(cargo_csv_data["origin_lat"])
    assert cargo.origin_location.lng == float(cargo_csv_data["origin_lng"])

    assert cargo.destination_location.city == cargo_csv_data["destination_city"]
    assert cargo.destination_location.state == cargo_csv_data["destination_state"]
    assert cargo.destination_location.lat == float(cargo_csv_data["destination_lat"])
    assert cargo.destination_location.lng == float(cargo_csv_data["destination_lng"])


def test_row_to_truck(truck_csv_data):
    truck = row_to_truck(**truck_csv_data)

    assert truck.truck == truck_csv_data["truck"]

    assert truck.location.city == truck_csv_data["city"]
    assert truck.location.state == truck_csv_data["state"]
    assert truck.location.lat == float(truck_csv_data["lat"])
    assert truck.location.lng == float(truck_csv_data["lng"])


@mock.patch("minimal_route_solver.commands.row_to_cargo")
@mock.patch("minimal_route_solver.commands.row_to_truck")
@mock.patch("minimal_route_solver.commands.persist_results")
@mock.patch("minimal_route_solver.commands.SolverByShortestOverallRoute")
def test_solve(mock_solver, mock_persist_results, mock_row_to_truck, mock_row_to_cargo):
    runner = CliRunner()
    cargo, truck = CargoFactory(), TruckFactory()
    mock_row_to_cargo.return_value = cargo
    mock_row_to_truck.return_value = truck

    with runner.isolated_filesystem():
        with open("cargos.csv", "w") as f:
            f.write("product\nLight bulbs")
        with open("trucks.csv", "w") as f:
            f.write("truck\nHartford Plastics Incartford")
        result = runner.invoke(solve, ["cargos.csv", "trucks.csv"])
        assert result.exit_code == 0

    mock_solver.assert_called_once_with([cargo], [truck])
    mock_solver.return_value.solve.assert_called_once_with()
    mock_persist_results.assert_called_once_with(
        mock.ANY, mock_solver.return_value.solve.return_value
    )


def test_persist_results():
    routes = RouteFactory.create_batch(10)

    expected_lines = ["cargo,truck,distance\r\n"] + [
        f"{route.cargo.product},{route.truck.truck},{round(route.distance, 2)}\r\n"
        for route in sorted(routes, key=lambda route: route.distance)
    ]

    output = StringIO()
    persist_results(output, routes)
    output.seek(0)
    lines = output.readlines()
    assert lines == expected_lines


def test_persist_results_manual(faker):
    routes = [
        RouteFactory(
            cargo=CargoFactory(product="first product"),
            truck=TruckFactory(truck="first truck"),
            distance=10.11111,
        ),
        RouteFactory(
            cargo=CargoFactory(product="second product"),
            truck=TruckFactory(truck="second truck"),
            distance=4.888888,
        ),
    ]

    expected_lines = [
        "cargo,truck,distance\r\n",
        "second product,second truck,4.89\r\n",
        "first product,first truck,10.11\r\n",
    ]

    output = StringIO()
    persist_results(output, routes)
    output.seek(0)
    lines = output.readlines()
    assert lines == expected_lines
