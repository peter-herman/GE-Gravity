from unittest import TestCase

from JsonExpressionTrees.JsonExpressionTree import JsonExpressionTree

__author__ = "Austin Drenski"
__project__ = "GE-Gravity"


class TestJsonExpressionTree(TestCase):
    def test_visit_0(self):
        e = JsonExpressionTree(lambda x: x * x)
        self.assertIsNotNone(e.tree)

    def test_visit_1(self):
        f = 10
        e = JsonExpressionTree(lambda x: f * x)
        self.assertIsNotNone(e.json)

    def test_visit_2(self):
        f = 10
        g = 0.1
        e = JsonExpressionTree(lambda x: g + f * x)
        self.assertIsNotNone(e.json_formatted)
