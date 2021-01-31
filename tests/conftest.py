import pytest

from string import ascii_uppercase


@pytest.fixture
def cargo_csv_data(faker):
    return {
        "product": faker.lexify("Product ???", letters=ascii_uppercase),
        "origin_city": faker.city(),
        "origin_state": faker.lexify("??", letters=ascii_uppercase),
        "origin_lat": str(faker.pydecimal(right_digits=7,min_value=-90,max_value=90)),
        "origin_lng": str(faker.pydecimal(right_digits=7,min_value=-180,max_value=180)),
        "destination_city": faker.city(),
        "destination_state": faker.lexify("??", letters=ascii_uppercase),
        "destination_lat": str(faker.pydecimal(right_digits=7,min_value=-90,max_value=90)),
        "destination_lng": str(faker.pydecimal(right_digits=7,min_value=-180,max_value=180)),
    }

@pytest.fixture
def truck_csv_data(faker):
    return {
        "truck": faker.lexify("Truck ???", letters=ascii_uppercase),
        "city": faker.city(),
        "state": faker.lexify("??", letters=ascii_uppercase),
        "lat": str(faker.pydecimal(right_digits=7,min_value=-90,max_value=90)),
        "lng": str(faker.pydecimal(right_digits=7,min_value=-180,max_value=180)),
    }
