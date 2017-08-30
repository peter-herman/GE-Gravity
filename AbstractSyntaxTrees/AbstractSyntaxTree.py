__author__ = "Austin Drenski"
__project__ = "GE-Gravity"

from ast import parse
from inspect import getsource
from json import dumps


def Serialize(function):
    sourceString = getsource(function)
    sourceExpression = parse(sourceString)
    sourceBody = sourceExpression.body

    jsonString = dumps(sourceBody)

    return jsonString
