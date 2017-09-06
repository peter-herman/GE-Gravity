import csv
from typing import List

from Examples.InputOutput.Country import *

__all__ = ["World", "read_world"]
__author__ = "Austin Drenski"
__project__ = "InputOutput"
__created__ = "9-6-2017"
__altered__ = "9-6-2017"
__version__ = "1.0.0"


class World(object):
    """
    Represents an experiment that is constructed with a specific parametrization and evaluated for given inputs.
    """

    __author__ = "Austin Drenski"

    __module__ = "InputOutput"

    __slots__ = ["_gdp", "_year", "_countries"]

    def __init__(self, gdp: float, year: str, countries: List[Country]) -> None:
        """
        Constructs an experiment with a specific parametrization.
        :param gdp: The alpha parameter.
        :param year: The beta parameter.
        """

        if gdp is None:
            raise TypeError

        if year is None:
            raise TypeError

        if countries is None:
            raise TypeError

        self._gdp = gdp
        self._year = year
        self._countries = countries

    def get_countries(self) -> List[Country]:
        return self._countries

    def find_country(self, country: str) -> Country:
        """
        Evaluates the derivative for a given input.
        :param country: The point at which the derivative is evaluated.
        :return: The value of the derivative at the given input.
        """

        if country is None:
            raise TypeError

        return next(
            filter(
                lambda x: x.get_name == country,
                self._countries),
            None)


def read_world(filePath: str) -> World:
    """
    Evaluates the experiment for a given input.
    :param filePath: The point at which the derivative is evaluated.
    :return: The value of the experiment at the given input.
    """

    if filePath is None:
        raise TypeError

    with open(filePath) as reader:
        lines = csv.DictReader(reader)
        countries = [Country(line["name"], float(line["gdp"]), line["year"]) for line in lines]

    gdp = sum([c._gdp for c in countries])

    return World(gdp, "2015", countries)
