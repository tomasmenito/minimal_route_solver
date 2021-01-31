from string import ascii_uppercase

import factory

from minimal_route_solver import models


class LocationFactory(factory.Factory):
    class Meta:
        model = models.Location

    city = factory.Faker("city")
    state = factory.Faker("lexify", text="??", letters=ascii_uppercase)
    lat = factory.Faker("pydecimal", right_digits=7, min_value=-90, max_value=90)
    lng = factory.Faker("pydecimal", right_digits=7, min_value=-180, max_value=180)


class CargoFactory(factory.Factory):
    class Meta:
        model = models.Cargo

    product = factory.Faker("lexify", text="Product ???", letters=ascii_uppercase)
    origin_location = factory.SubFactory(LocationFactory)
    destination_location = factory.SubFactory(LocationFactory)


class TruckFactory(factory.Factory):
    class Meta:
        model = models.Truck

    truck = factory.Faker("lexify", text="Truck ???", letters=ascii_uppercase)
    location = factory.SubFactory(LocationFactory)


class RouteFactory(factory.Factory):
    class Meta:
        model = models.Route

    truck = factory.SubFactory(TruckFactory)
    cargo = factory.SubFactory(CargoFactory)
    distance = factory.Faker("pyfloat", positive=True)
