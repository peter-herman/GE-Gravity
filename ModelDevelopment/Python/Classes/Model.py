from functools import partial
from time import time
from typing import Callable, Iterable, List, Tuple

import numpy as np
from scipy.optimize import root

from ModelDevelopment.Python.Classes.Country import Country

__author__ = "Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "10-4-2017"
__altered__ = "10-10-2017"
__version__ = "1.0.0"


class Model(object):
    """
    Represents a gravity model.
    """

    __slots__ = [
        "equation",
        "records",
        "normalized_name",
        "last_solution_time",
        "last_solution_success"
    ]

    def __init__(self, records: List[Country], normalized_name: str, equation: Callable[[List[Country], int, List[float]], Iterable[float]]) -> None:
        self.records = records
        self.normalized_name = normalized_name
        self.equation = partial(equation, records, [x.name for x in records].index(normalized_name))
        self.last_solution_time = 0
        self.last_solution_success = False

    def solve(self, x0: List[float] = None, method: str = "hybr", tol: float = 1e-8, xtol: float = 1e-8, maxfev: int = 1400) -> Iterable[Tuple[str, float, float]]:
        """
        This function wraps the optimization and result construction tasks.
        :param x0:
        :param method:
        :param tol:
        :param xtol:
        :param maxfev:
        :return:
        """

        if x0 is None:
            x0 = np.ones(2 * len(self.records))

        if not isinstance(x0, np.ndarray):
            x0 = np.asarray(x0)

        start = time()

        results = root(fun=self.equation, x0=x0, method=method, tol=tol, options={"xtol": xtol, "maxfev": maxfev})

        self.last_solution_time = time() - start

        self.last_solution_success = results.success

        return self.__normalize_baseline(results.x)

    def __normalize_baseline(self, results: List[float], inward: bool = True) -> Iterable[Tuple[str, float, float]]:
        """
        This function takes the raw results from the optimization routine and constructs a list of tuples to return to the user.
        :param results: The results of the optimization.
        :param inward: True if the normalized entry is an inward resistance term; otherwise false.
        :return: A list of tuples containing inward and outward multilateral resistance terms by country.
        """

        if not isinstance(results, list):
            results = list(results)

        count = len(results) // 2

        inward_resistances = results[:count]

        outward_resistances = 1000 * results[count:]

        return zip([x.name for x in self.records], inward_resistances, outward_resistances)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        pass
