"""
The gravity equation for baseline multilateral resistance terms.
"""
from typing import List

from ModelDevelopment.Python.Classes.Country import Country

__author__ = "Serge Shikher, Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "10-11-2017"
__altered__ = "10-13-2017"
__version__ = "1.0.0"


def system_for_multilateral_resistance(countries: List[Country], x: List[float]) -> List[float]:
    """
    This is the function we will pass to the model. It takes two arguments that the model will bind with data elements.

    This function returns zeroes when the solution to the system is provided as the argument.

    :param countries: A collection of country data.
    :param x: The argument vector supplied by the optimization routine.
    :return: An iterable collection of values.
    """

    count = len(countries)

    imr = [0] * count
    omr = [0] * count

    for i in range(count):
        name = countries[i].name
        imr[i] = x[i] * sum(1000 * x[j + count] * countries[j].export_cost_by_output_share[name] for j in range(count))

    for i in range(count):
        name = countries[i].name
        omr[i] = 1000 * x[i + count] * sum(x[j] * countries[j].import_cost_by_expenditure_share[name] for j in range(count))

    return [1 - item for item in imr + omr]
