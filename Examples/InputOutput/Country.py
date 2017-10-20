__all__ = ["Country"]
__author__ = "Austin Drenski"
__project__ = "InputOutput"
__created__ = "9-6-2017"
__altered__ = "9-11-2017"
__version__ = "1.1.0"


class Country(object):
    """
    Represents an experiment that is constructed with a specific parametrization and evaluated for given inputs.
    """

    __author__ = "Austin Drenski"

    __module__ = "InputOutput"

    __slots__ = ["_name", "_gdp", "_year"]

    @property
    def name(self) -> str:
        """
        Gets the name of the observation.
        :return: The name of the observation.
        """

        return self._name

    @property
    def gdp(self) -> float:
        """
        Gets the GDP of the observation.
        :return: The GDP of the observation.
        """

        return self._gdp

    @property
    def year(self) -> str:
        """
        Gets the year of the observation.
        :return: The year of the observation.
        """

        return self._year

    def __init__(self, name: str, gdp: float, year: str) -> None:
        """
        Constructs an experiment with a specific parametrization.
        :param name: The country name.
        :param gdp: The annual GDP of the observation.
        :param year: The year of observation.
        """

        if name is None:
            raise TypeError

        if gdp is None:
            raise TypeError

        if year is None:
            raise TypeError

        self._name = name
        self._gdp = gdp
        self._year = year

    def __str__(self) -> str:
        return (self._name, self._year, self._gdp).__str__()

    def __repr__(self) -> str:
        return self.__str__()
