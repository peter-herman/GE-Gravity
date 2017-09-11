from Examples.InputOutput.World import *

filePath = "\\users\\austin.drenski\\desktop\\gravity_programming_sample_data.txt"

world = read_world(filePath)

world.countries
world.find_country("USA")
world.find_gdp("2014")
world.find_gdp("2015")
