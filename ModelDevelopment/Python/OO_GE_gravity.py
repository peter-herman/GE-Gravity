"""
Demonstrates how to use the proposed API to solve for baseline multilateral resistance terms.
"""
from ModelDevelopment.Python.Classes.Model import Model
from ModelDevelopment.Python.DataConstruction import Construct
from ModelDevelopment.Python.Equation import system_for_multilateral_resistance

__author__ = "Serge Shikher, Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "9-25-2017"
__altered__ = "10-13-2017"
__version__ = "1.2.0"

countries = Construct("G:/data/Gravity Resources/Gravity modeling in Python/GE gravity 10.3.2017/ge_ppml_data.dta")

model = Model(countries=countries, normalized_name="ZZZ", equation=system_for_multilateral_resistance)

print(model.solve(x0=[0] * 82))
print(model.time_elapsed)
print(model.is_valid)

print(model.solve(x0=[1] * 82))
print(model.time_elapsed)
print(model.is_valid)

print(model.solve(x0=[2] * 82))
print(model.time_elapsed)
print(model.is_valid)

print(model.solve(x0=[3] * 82))
print(model.time_elapsed)
print(model.is_valid)

result = model.solve()
sum(value * value for value in system_for_multilateral_resistance(countries, [x.inward for x in result] + [x.outward for x in result]))
