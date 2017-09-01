from unittest import TestCase

from JsonExpressionTrees.JsonExpressionTree import JsonExpressionTree

__author__ = "Austin Drenski"
__project__ = "GE-Gravity.JsonExpressionTrees"
__created__ = "8-30-2017"
__altered__ = "8-31-2017"
__version__ = "1.0.0"


def outer_func(x: int, y: int) -> int:
    return abs(x) ** y


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

    def test_visit_3(self) -> None:

        f = 10

        e = JsonExpressionTree(lambda x: outer_func(f, x))

        print(e.json_formatted)

        self.assertIsNotNone(e.json_formatted)

    def test_visit_4(self) -> None:
        import ast
        import inspect

        f = lambda x, y: outer_func(x, y)

        g = ast.parse(inspect.getsource(f).strip())

        for g0 in g.body:
            for g1 in g0.targets:
                print("g1.id: {0}".format(g1.id))
                print("g1.ctx: {0}".format(g1.ctx))
                print("g1: {0}".format(JsonExpressionTree.visit(g1)))
