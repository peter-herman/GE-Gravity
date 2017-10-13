"""
Demonstrates how to use the proposed API to solve for baseline multilateral resistance terms.
"""
from ModelDevelopment.Python.Classes.Model import Model
from ModelDevelopment.Python.DataConstruction import Construct
from ModelDevelopment.Python.Equation import calculate_multilateral_resistance

__author__ = "Serge Shikher, Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "9-25-2017"
__altered__ = "10-11-2017"
__version__ = "1.2.0"

countries = Construct("G:/data/Gravity Resources/Gravity modeling in Python/GE gravity 10.3.2017/ge_ppml_data.dta")

model = Model(countries=countries, normalized_name="ZZZ", equation=calculate_multilateral_resistance)

result = model.solve()

print(result)
print(model.time_elapsed)
print(model.is_valid)
