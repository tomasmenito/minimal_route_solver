from abc import ABC, abstractmethod
from typing import Iterable

from .models import Cargo, Route, Truck


class MinimalRouteSolver(ABC):
    def __init__(self, cargos: Iterable[Cargo], trucks: Iterable[Truck]):
        self.cargos = cargos
        self.trucks = trucks

    @abstractmethod
    def solve(self) -> list[Route]:
        pass


class SolverByMinimalOverallRoute(MinimalRouteSolver):
    def solve(self) -> list[Route]:
        return []
