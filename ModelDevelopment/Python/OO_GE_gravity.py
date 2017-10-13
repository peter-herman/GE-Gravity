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


def func_base_mr1(records: List[Country], x: List[float]) -> Iterable[float]:
    """
    This is the function we will pass to the model. It takes three arguments that the model will bind with data elements.
    :param records: A collection of country data.
    :param x: The argument vector supplied by the optimization routine.
    :return: An iterable collection of values.
    """

    count = len(records)

    imr = [0] * count
    omr = [0] * count

    for i in range(count):
        name = records[i].name
        imr[i] = x[i] * sum(x[j + count] * records[j].export_cost_by_output_share[name] for j in range(count))

    for i in range(count):
        name = records[i].name
        omr[i] = x[i + count] * sum(x[j] * records[j].import_cost_by_expenditure_share[name] for j in range(count))

    return [1 - 1000 * item for item in imr + omr]


countries = Construct("G:/data/Gravity Resources/Gravity modeling in Python/GE gravity 10.3.2017/ge_ppml_data.dta")

model = Model(countries=countries, normalized_name="ZZZ", equation=func_base_mr1)

result = model.solve()

print(model.time_elapsed)
print(model.is_valid)
