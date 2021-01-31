from itertools import chain

from minimal_route_solver.solvers import SolverByShortestOverallRoute
from tests.factories import CargoFactory, RouteFactory, TruckFactory


def test_generate_sorted_shorted_routes_by_cargo():
    cargos = CargoFactory.create_batch(10)
    trucks = TruckFactory.create_batch(5)

    routes = SolverByShortestOverallRoute(
        cargos, trucks
    ).generate_sorted_shortest_routes_by_cargo(cargos[0])

    assert len(routes) == len(trucks)
    assert all(
        routes[i].distance <= routes[i + 1].distance for i in range(len(routes) - 1)
    )
    assert {route.truck for route in routes} == set(trucks)


def test_find_shortest_route_no_busy_trucks():
    cargos = CargoFactory.create_batch(5)
    routes_by_cargo = {
        cargo: sorted(
            RouteFactory.create_batch(5, cargo=cargo), key=lambda r: r.distance
        )
        for cargo in cargos
    }
    busy_trucks = set()

    shortest_route = SolverByShortestOverallRoute.find_shortest_route(
        routes_by_cargo, busy_trucks
    )

    all_routes = chain.from_iterable(routes_by_cargo.values())
    assert all(shortest_route.distance <= route.distance for route in all_routes)


def test_find_shortest_route_with_busy_trucks():
    cargos = CargoFactory.create_batch(5)
    trucks = TruckFactory.create_batch(10)

    routes_by_cargo = {}
    for cargo in cargos:
        routes = sorted(
            [RouteFactory(truck=truck, cargo=cargo) for truck in trucks],
            key=lambda route: route.distance,
        )
        routes_by_cargo[cargo] = routes

    all_routes = list(chain.from_iterable(routes_by_cargo.values()))

    shortest_route_without_busy = min(all_routes, key=lambda route: route.distance)
    busy_trucks = {shortest_route_without_busy.truck}
    shortest_route = SolverByShortestOverallRoute.find_shortest_route(
        routes_by_cargo, busy_trucks
    )

    assert shortest_route != shortest_route_without_busy
    assert all(
        shortest_route.distance <= route.distance
        for route in all_routes
        if route.truck not in busy_trucks
        and route.cargo != shortest_route_without_busy.cargo
    )


def test_solve():
    cargos = CargoFactory.create_batch(6)
    trucks = TruckFactory.create_batch(10)

    solution = SolverByShortestOverallRoute(cargos, trucks).solve()

    assert len(solution) == len(cargos)
    assert {route.cargo for route in solution} == set(cargos)
