from functools import partial
from time import time
from typing import Callable, List, NamedTuple, Sequence, Union

import numpy as np
from scipy.optimize import root

from ModelDevelopment.Python.Classes.Country import Country

__author__ = "Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "10-4-2017"
__altered__ = "10-13-2017"
__version__ = "1.2.0"


class ModelResult(NamedTuple):
    """
    Represents a model result for one country.
    """
    country: str
    inward: float
    outward: float


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
    def count(self) -> int:
        return len(self.__countries)

    @property
    def countries(self) -> Sequence[Country]:
        """
        The collection of countries in the model.
        """
        return [x for x in self.__countries]

    @property
    def is_valid(self) -> bool:
        """
        True if the previous solution was successful; otherwise false.
        """
        return self.__is_valid

    @property
    def normalized_index(self) -> int:
        """
        The index of the country to which the results are normalized.
        """
        return [x.name for x in self.__countries].index(self.__normalized_name)

    @property
    def normalized_name(self) -> str:
        """
        The name of the country to which the results are normalized.
        """
        return self.__normalized_name

    @property
    def time_elapsed(self) -> int:
        """
        The time elapsed during the previous solution.
        """
        return self.__time_elapsed

    def __init__(self, countries: Sequence[Country], normalized_name: str, equation: Callable[[List[Country], List[float]], List[float]]) -> None:
        self.__countries = list(countries)

        if len(self.__countries) == 0:
            raise ValueError("The country collection is empty.")

        if [x.name for x in countries].index(normalized_name) < 0:
            raise ValueError("{0} not found in country collection".format(normalized_name))

        self.__normalized_name = normalized_name
        self.__equation = self.__wrap_equation(equation)
        self.__time_elapsed = 0
        self.__is_valid = False

    def solve(self, x0: Sequence[float] = None, method: str = "hybr", tol: float = 1e-8, xtol: float = 1e-8,
              maxfev: int = 1400) -> Sequence[ModelResult]:
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

        if len(x0) != 2 * len(self.__countries):
            raise ValueError("Expected sequence of {0} values, but received {1} values.".format(len(self.__countries), len(x0)))

        start = time()

        results = root(fun=self.__equation, x0=x0, method=method, tol=tol, options={"xtol": xtol, "maxfev": maxfev})

        self.__time_elapsed = time() - start
        self.__is_valid = results.success

        return self.__normalize_baseline(results.x)

    def __wrap_equation(self, equation: Callable[[List[Country], List[float]], List[float]]) -> Callable[[List[float]], List[float]]:
        """
        This function wraps the user-defined delegate to handle normalizing to the specified country.
        :param equation: The user-defined delegate.
        :return: A function suitable for use in the solve() function.
        """

        bound_function = partial(equation, self.__countries)
        normalized_index = self.normalized_index

        def __wrapped_function(x: List[float]) -> List[float]:
            x[normalized_index] = 1.0
            result = bound_function(x)
            result[normalized_index] = 0.0
            return result

        return __wrapped_function

    def __normalize_baseline(self, results: Sequence[float]) -> Sequence[ModelResult]:
        """
        This function takes the raw results from the optimization routine and constructs a list of tuples to return to the user.
        :param results: The results of the optimization.
        :return: A list of tuples containing inward and outward multilateral resistance terms by country.
        """

        if not isinstance(results, list):
            results = list(results)

        count = len(self.__countries)

        inward_resistances = (x for x in results[:count])

        outward_resistances = (x for x in results[count:])

        names = (x.name for x in self.__countries)

        return [ModelResult(x[0], x[1], x[2]) for x in iter(zip(names, inward_resistances, outward_resistances))]

    def __getitem__(self, item: Union[str, int]) -> Country:
        if isinstance(item, str):
            return next(x for x in self.__countries if x.name == item)

        if isinstance(item, int):
            return self.__countries[item]

    def __contains__(self, item: str) -> bool:
        return any(x.name is item for x in self.__countries)

    def __eq__(self, other: 'Model') -> bool:

        if hash(self.__equation) != hash(other.__equation):
            return False

        if self.__normalized_name != other.__normalized_name:
            return False

        if len(self.__countries) != len(other.__countries):
            return False

        for i in range(len(self.__countries)):
            if self.__countries[i] != other.__countries[i]:
                return False

        return True

    def __ne__(self, other: 'Model') -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__countries) + hash(self.__normalized_name) + hash(self.__equation)

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return "(normalized_name:{0}, success: {1}, elapsed: {2})".format(self.__normalized_name, self.__is_valid, self.__time_elapsed)
