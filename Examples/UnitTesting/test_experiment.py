from unittest import TestCase

from Examples.UnitTesting.Experiment import Experiment

__author__ = "Austin Drenski"
__project__ = "UnitTesting"


class TestExperiment(TestCase):
    """
    Unit tests for the Experiment class.
    """

    def test_evaluate_derivative(self):
        pass

    def test_evaluate(self):
        # Arrange
        experiment = Experiment(0, 0)

        # Act
        result = experiment.evaluate(1)

        # Assert
        self.assertEqual(1, result)
