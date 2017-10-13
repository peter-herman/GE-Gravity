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
        "__equation",
        "__countries",
        "__normalized_name",
        "__time_elapsed",
        "__is_valid"
    ]

    @property
    def normalized_name(self) -> str:
        """
        The name of the country to which the results are normalized.
        """
        return self.__normalized_name

    @property
    def normalized_index(self) -> int:
        """
        The index of the country to which the results are normalized.
        """
        return [x.name for x in self.__countries].index(self.__normalized_name)

    @property
    def countries(self) -> Iterable[Country]:
        """
        The collection of countries in the model.
        """
        return (x for x in self.__countries)

    @property
    def time_elapsed(self):
        """
        The time elapsed during the previous solution.
        """
        return self.__time_elapsed

    @property
    def is_valid(self):
        """
        True if the previous solution was successful; otherwise false.
        """
        return self.__is_valid

    def __init__(self, countries: Iterable[Country], normalized_name: str,
                 equation: Callable[[Iterable[Country], List[float]], Iterable[float]]) -> None:
        self.__countries = list(countries)

        if len(self.__countries) == 0:
            raise ValueError("The country collection is empty.")

        if [x.name for x in countries].index(normalized_name) < 0:
            raise ValueError("{0} not found in country collection".format(normalized_name))

        self.__normalized_name = normalized_name
        self.__equation = partial(equation, self.__countries)
        self.__time_elapsed = 0
        self.__is_valid = False

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
            x0 = np.ones(2 * len(self.__countries))

        if not isinstance(x0, np.ndarray):
            x0 = np.asarray(x0)

        start = time()

        results = root(fun=self.__equation, x0=x0, method=method, tol=tol, options={"xtol": xtol, "maxfev": maxfev})

        self.__time_elapsed = time() - start
        self.__is_valid = results.success

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

        count = len(self.__countries)

        base = results[self.normalized_index if inward else self.normalized_index + count]

        inward_resistances = (x / base for x in results[:count])

        outward_resistances = (x / base for x in results[count:])

        names = (x.name for x in self.__countries)

        return list(zip(names, inward_resistances, outward_resistances))

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return "(normalized_name:{0}, success: {1}, elapsed: {2})".format(self.__normalized_name, self.__is_valid,
                                                                          self.__time_elapsed)
