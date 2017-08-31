from unittest import TestCase

from JsonExpressionTrees.JsonExpressionTree import JsonExpressionTree

__author__ = "Austin Drenski"
__project__ = "GE-Gravity.JsonExpressionTrees"
__created__ = "8-30-2017"
__altered__ = "8-31-2017"
__version__ = "1.0.0"


class TestJsonExpressionTree(TestCase):
    def test_visit_0(self) -> None:

        e = JsonExpressionTree(lambda x: x * x)

        self.assertIsNotNone(e.tree)

    def test_visit_1(self) -> None:

        f = 10

        e = JsonExpressionTree(lambda x: f * x)

        self.assertIsNotNone(e.json)

    def test_visit_2(self) -> None:

        f = 10

        g = 0.1

        e = JsonExpressionTree(lambda x: g + f * x)

        self.assertIsNotNone(e.json_formatted)
