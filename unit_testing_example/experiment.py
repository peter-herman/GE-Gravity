__author__ = "Austin Drenski"
__project__ = "unit_testing_example"


class Experiment(object):
    """
    Represents an experiment that is constructed with a specific parameterization and evaluated for given inputs.
    """

    def __init__(self, a, b):
        """
        Constructs an experiment with a specific parameterization.
        :param a: The alpha parameter.
        :param b: The beta parameter.
        """

        self.a = a
        self.b = b

    def evaluate_derivative(self, x):
        """
        Evaluates the derivative for a given input.
        :param x: The point at which the derivative is evaluated.
        :return: The value of the derivative at the given input.
        """

        return x - self.b

    def evaluate(self, x):
        """
        Evaluates the experiment for a given input.
        :param x: The point at which the derivative is evaluated.
        :return: The value of the experiment at the given input.
        """

        return (x * x) * self.evaluate_derivative(x) - self.a




