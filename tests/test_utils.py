import pytest

from minimal_route_solver.utils import calculate_haversine_distance
from tests.factories import LocationFactory


def test_calculate_haversine_distance():
    new_york = LocationFactory(
        city="New York", state="NY", lat=40.7134096124597, lng=-74.00457854001111
    )
    san_francisco = LocationFactory(
        city="San Francisco", state="CA", lat=37.78897091052155, lng=-122.41039209461564
    )

    expected_miles = pytest.approx(2564.9, 0.1)

    assert calculate_haversine_distance(new_york, san_francisco) == expected_miles
    assert calculate_haversine_distance(san_francisco, new_york) == expected_miles
