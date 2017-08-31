from typing import TypeVar

__all__ = ["Experiment"]
__author__ = "Austin Drenski"
__project__ = "UnitTesting"
__created__ = "8-22-2017"
__altered__ = "8-31-2017"
__version__ = "1.0.1"


class Experiment(object):
    """
    Represents an experiment that is constructed with a specific parametrization and evaluated for given inputs.
    """

    __author__ = "Austin Drenski"

    __module__ = "UnitTesting"

    __slots__ = ["_a", "_b"]

    _T = TypeVar("T", int, float)

    def __init__(self, a: _T, b: _T) -> None:
        """
        Constructs an experiment with a specific parametrization.
        :param a: The alpha parameter.
        :param b: The beta parameter.
        """

        if a is None:
            raise TypeError

        if b is None:
            raise TypeError

        self._a = a
        self._b = b

    def evaluate(self, x: _T) -> _T:
        """
        Evaluates the experiment for a given input.
        :param x: The point at which the derivative is evaluated.
        :return: The value of the experiment at the given input.
        """

        if x is None:
            raise TypeError

        return (x * x) * self.evaluate_derivative(x) - self._a

    def evaluate_derivative(self, x: _T) -> _T:
        """
        Evaluates the derivative for a given input.
        :param x: The point at which the derivative is evaluated.
        :return: The value of the derivative at the given input.
        """

        if x is None:
            raise TypeError

        return x - self._b
