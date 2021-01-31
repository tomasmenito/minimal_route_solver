# Minimal route solver

The minimal route solver receives a list of cargos that must be transported with origin and destination and a list of trucks with their location.

The trucks can only make one trip and only carry one cargo.

The goal with this implementation was to focus more on data structures and loops than in the algorithm itself.
The chosen algorithm was:
1. Use an aerial distance matrix using haversine distance calculator for all distance calculations, using lat and lng only.
2. Calculate a sorted list (by distance ASC) of all possible routes for every cargo (one for each truck).
3. Loop until there are no cargos left, choosing the shortest overall route.
4. When a route is chosen, the vehicle can no longer be used by other routes, so we ignore all routes containing that vehicle, as well as all routes from the chosen cargo.

The structure was made using interfaces making easy to add new distance matrix calculators or solvers.

## Installation

This project uses Poetry to manage dependencies, to install check [Poetry installation docs](https://python-poetry.org/docs/#installation/).

To install dependencies
```bash
poetry install
```
## Commands

To test run
```shell
make test
```

To calculate results run:
```shell
poetry run cargo_truck cargos_file.csv trucks_file.csv [results_file.csv]
```

To get help run
```shell
poetry run cargo_truck --help
```
## Possible improvements

- [ ] Create bruteforce solver (for benchmarking or solving small problems)
- [ ] Write docstrings for complex methods
- [ ] Use logs to follow process
- [ ] Write other distance matrix calculators (calculating real route for an example)
- [ ] Write other solvers with other algorithms
- [ ] Add new commands to choose distance matrix and solver implementations on command line (or envvars)
- [ ] Usage of asyncio for IO bound tasks (if present)
