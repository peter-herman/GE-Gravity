from unittest import TestCase

from experiment import Experiment

__author__ = "Austin Drenski"
__project__ = "UnitTestingExample"


class TestExperiment(TestCase):
    """
    Unit tests for the Experiment class.
    """

    def test_evaluate_derivative(self):
        self.fail()

    def test_evaluate(self):
        # Arrange
        experiment = Experiment(0, 0)

        # Act
        result = experiment.evaluate(1)

        # Assert
        self.assertEqual(1, result)
