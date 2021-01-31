from unittest import mock

from minimal_route_solver.distance_matrix import LazyAerialDistanceMatrix
from tests.factories import LocationFactory


@mock.patch("minimal_route_solver.distance_matrix.calculate_haversine_distance")
def test_lazy_aerial_calls(mock_calculate_distance, faker):
    mock_calculate_distance.return_value = faker.pyfloat(positive=True)

    origin, destination = LocationFactory(), LocationFactory()
    distance_matrix = LazyAerialDistanceMatrix()

    result = distance_matrix.distance(origin, destination)

    assert result == mock_calculate_distance.return_value

    mock_calculate_distance.assert_called_once()
    assert {*mock_calculate_distance.call_args.args} == {origin, destination}


@mock.patch("minimal_route_solver.distance_matrix.calculate_haversine_distance")
def test_lazy_aerial_call_repeated_optimization(mock_calculate_distance, faker):
    mock_calculate_distance.return_value = faker.pyfloat(positive=True)

    origin, destination = LocationFactory(), LocationFactory()
    distance_matrix = LazyAerialDistanceMatrix()

    first_result = distance_matrix.distance(origin, destination)
    second_result = distance_matrix.distance(origin, destination)

    assert first_result == mock_calculate_distance.return_value
    assert second_result == mock_calculate_distance.return_value

    mock_calculate_distance.assert_called_once()


@mock.patch("minimal_route_solver.distance_matrix.calculate_haversine_distance")
def test_lazy_aerial_call_switching_origin_destination_optimization(
    mock_calculate_distance, faker
):
    mock_calculate_distance.return_value = faker.pyfloat(positive=True)

    origin, destination = LocationFactory(), LocationFactory()
    distance_matrix = LazyAerialDistanceMatrix()

    first_result = distance_matrix.distance(origin, destination)
    second_result = distance_matrix.distance(destination, origin)

    assert first_result == mock_calculate_distance.return_value
    assert second_result == mock_calculate_distance.return_value

    mock_calculate_distance.assert_called_once()


@mock.patch("minimal_route_solver.distance_matrix.calculate_haversine_distance")
def test_lazy_aerial_multiple_calls(mock_calculate_distance, faker):
    first_distance, second_distance = faker.pyfloat(positive=True), faker.pyfloat(
        positive=True
    )
    mock_calculate_distance.side_effect = [first_distance, second_distance]

    first_origin, first_destination = LocationFactory(), LocationFactory()
    second_origin, second_destination = LocationFactory(), LocationFactory()
    distance_matrix = LazyAerialDistanceMatrix()

    first_result = distance_matrix.distance(first_origin, first_destination)
    second_result = distance_matrix.distance(second_origin, second_destination)

    assert first_result == first_distance
    assert second_result == second_distance

    assert mock_calculate_distance.call_count == 2
