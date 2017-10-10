"""
Estimates the gravity equation and solves for baseline multilateral resistance terms.
"""
from typing import Iterable, List

from ModelDevelopment.Python.Classes.Country import Country
from ModelDevelopment.Python.Classes.Model import Model
from ModelDevelopment.Python.DataConstruction import Construct

__author__ = "Serge Shikher, Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "9-25-2017"
__altered__ = "10-10-2017"
__version__ = "1.1.0"


def func_base_mr1(records: List[Country], normal_index: int, x: List[float]) -> Iterable[float]:
    """
    This is the function we will pass to the model. It takes three arguments that the model will bind with data elements.
    :param records: A collection of country data.
    :param normal_index: The index in the country data collection of the normalized country.
    :param x: The argument vector supplied by the optimization routine.
    :return: An iterable collection of values.
    """

    count = len(records)

    imr = [0] * count
    omr = [0] * count

    for i in range(count):
        name = records[i].name
        imr[i] = x[i] * sum([records[j].export_cost_by_output_share[name] * x[j + count] for j in range(count)])

    x[normal_index] = 1

    for i in range(count):
        name = records[i].name
        omr[i] = x[i + count] * sum([records[j].import_cost_by_expenditure_share[name] * x[j] for j in range(count)])

    return [1 - 1000 * item for item in imr + omr]


countries = Construct("G:/data/Gravity Resources/Gravity modeling in Python/GE gravity 10.3.2017/ge_ppml_data.dta")

model = Model(records=countries, normalized_name="ZZZ", equation=func_base_mr1)

result = model.solve()

print(model.last_solution_success)
print(model.last_solution_time)
