import csv
from itertools import groupby
from typing import List, Tuple

from Examples.InputOutput.Country import *

__all__ = ["World", "read_world"]
__author__ = "Austin Drenski"
__project__ = "InputOutput"
__created__ = "9-6-2017"
__altered__ = "9-11-2017"
__version__ = "1.1.0"


class World(object):
    """
    Represents an experiment that is constructed with a specific parametrization and evaluated for given inputs.
    """

    __author__ = "Austin Drenski"

    __module__ = "InputOutput"

    __slots__ = ["_annualGDP", "_countries"]

    @property
    def annualGDP(self) -> List[Tuple[str, float]]:
        return self._annualGDP

    @property
    def countries(self) -> List[Country]:
        return self._countries

    def __init__(self, annualGDP: List[Tuple[str, float]], countries: List[Country]) -> None:
        """
        Constructs a world of countries.
        :param annualGDP: A collection of tuples containing a year and the global GDP in that year.
        :param countries: The countries in this world.
        """

        if annualGDP is None:
            raise TypeError

        if countries is None:
            raise TypeError

        self._annualGDP = annualGDP
        self._countries = countries

    def find_country(self, name: str) -> Country:
        """
        Finds the country with the given name.
        :param name: The country to locate.
        :return: The country whose name was given.
        """

        if name is None:
            raise TypeError

        return next(filter(lambda x: x.name == name, self._countries), None)

    def find_gdp(self, year: str) -> float:
        """
        Finds the country with the given name.
        :param year: The year for which to locate GDP.
        :return: The global GDP of the given year.
        """

        if year is None:
            raise TypeError

        return sum([country.gdp for country in filter(lambda x: x.year == year, self._countries)])


def read_world(filePath: str) -> World:
    """
    Reads countries from a file and returns a world.
    :param filePath: The file containing countries.
    :return: A world constructed from the countries in the file.
    """

    if filePath is None:
        raise TypeError

    with open(filePath, encoding="utf-8-sig") as reader:
        lines = csv.DictReader(reader)
        countries = [Country(line["name"], float(line["gdp"]), line["year"]) for line in lines]

    annualGDP = [(key, sum([country.gdp for country in group])) for key, group in groupby(countries, lambda x: x.year)]

    return World(annualGDP, countries)
