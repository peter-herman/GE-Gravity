import ast
import inspect
import json

__all__ = ["JsonExpressionTree"]
__author__ = "Austin Drenski"
__project__ = "GE-Gravity.JsonExpressionTrees"
__created__ = "8-30-2017"
__altered__ = "8-31-2017"
__version__ = "1.0.0"


class JsonExpressionTree(object):
    """
    Represents an abstract syntax tree serialized into JSON.

    This class is modeled after the Expression class in the .NET Framework. The idea is to serialize a Python expression
    into a well-defined form that can be sent over the wire to a remote compute server. On the server-side, the JSON
    expression tree will be deserialized as a .NET Expression object and compiled to a function delegate.
    """

    __author__ = "Austin Drenski"

    __module__ = "JsonExpressionTrees"

    __slots__ = ["_json", "_json_formatted", "_source", "_tree"]

    @property
    def tree(self) -> dict:
        """
        Gets the abstract syntax tree created by this JsonExpressionTree.
        :return: The abstract syntax tree.
        """

        return self._tree

    @property
    def json(self) -> str:
        """
        Gets the JSON abstract syntax tree created by this JsonExpressionTree.
        :return: The JSON abstract syntax tree.
        """

        return self._json

    @property
    def json_formatted(self) -> str:
        """
        Gets the formatted JSON abstract syntax tree created by this JsonExpressionTree.
        :return: The formatted JSON abstract syntax tree.
        """

        return self._json_formatted

    def __init__(self, func: callable) -> None:
        """
        Constructs a JsonExpressionTree from a given function.
        :param func: a function to be serialized.
        """

        if func is None:
            raise TypeError

        self._source = inspect.getsource(func).strip()
        self._tree = self.visit(ast.parse(self._source))
        self._json = json.dumps(self._tree, separators=(",", ":"))
        self._json_formatted = json.dumps(self._tree, indent=2)

    @staticmethod
    def visit(node: ast.AST) -> dict:
        """
        Visits a node in the abstract syntax tree and recursively dispatches by node type.
        :param node: The node to visit.
        :return: The serialized representation of the node and any descendants.
        """

        if node is None:
            raise TypeError

        if isinstance(node, ast.Module):
            return JsonExpressionTree.visit(node.body[0].value)

        elif isinstance(node, ast.Lambda):
            return JsonExpressionTree.visit(node.body)

        elif isinstance(node, int) or isinstance(node, float):
            return JsonExpressionTree._constant_node(node)

        elif isinstance(node, ast.Num):
            return JsonExpressionTree._constant_node(node.n)

        elif isinstance(node, ast.Name):
            localsLookup = locals()

            globalLookup = globals()

            name = node.id

            if name in localsLookup:
                return JsonExpressionTree.visit(localsLookup[name])

            elif name in globalLookup:
                return JsonExpressionTree.visit(globalLookup[name])

            return JsonExpressionTree._parameter_node(name)

        elif isinstance(node, ast.UnaryOp):
            return JsonExpressionTree._unary_node(
                JsonExpressionTree.visit(node.op),
                JsonExpressionTree.visit(node.operand))

        elif isinstance(node, ast.BinOp):
            return JsonExpressionTree._binary_node(
                JsonExpressionTree.visit(node.op),
                JsonExpressionTree.visit(node.left),
                JsonExpressionTree.visit(node.right))

        elif isinstance(node, ast.Call):
            if len(node.args) == 1:
                return JsonExpressionTree._unary_node(
                    JsonExpressionTree.visit(node.func),
                    JsonExpressionTree.visit(node.args[0]))

            elif len(node.args) == 2:
                return JsonExpressionTree._binary_node(
                    JsonExpressionTree.visit(node.func),
                    JsonExpressionTree.visit(node.args[0]),
                    JsonExpressionTree.visit(node.args[1]))
            else:
                return JsonExpressionTree._unknown_node(repr(node))

        return JsonExpressionTree._unknown_node(repr(node))

    @staticmethod
    def _constant_node(value: float) -> dict:

        if value is None:
            raise TypeError

        return {
            "type": "constant",
            "value": value
        }

    @staticmethod
    def _parameter_node(name: str) -> dict:

        if name is None:
            raise TypeError

        return {
            "type": "parameter",
            "name": name
        }

    @staticmethod
    def _unary_node(operator: dict, operand_0: dict) -> dict:

        if operator is None:
            raise TypeError

        if operand_0 is None:
            raise TypeError

        return {
            "type": "unary",
            "operator": operator,
            "operand_0": operand_0
        }

    @staticmethod
    def _binary_node(operator: dict, operand_0: dict, operand_1: dict) -> dict:

        if operator is None:
            raise TypeError

        if operand_0 is None:
            raise TypeError

        if operand_1 is None:
            raise TypeError

        return {
            "type": "binary",
            "operator": operator,
            "operand_0": operand_0,
            "operand_1": operand_1
        }

    @staticmethod
    def _unknown_node(unknown: object) -> dict:

        if unknown is None:
            raise TypeError

        return {
            "type": "unknown",
            "object": unknown
        }

    def __repr__(self) -> str:

        return self._json

    def __str__(self) -> str:

        return self._json_formatted

    def __eq__(self, other) -> bool:

        if other is JsonExpressionTree:
            return self.tree == other.tree

        if other is dict:
            return self._tree == other

        if other is str:
            return self._json == other

        return False

    def __ne__(self, other) -> bool:

        return not self.__eq__(other)

    def __bool__(self) -> bool:

        return self._tree is not None

    def __hash__(self) -> int:

        return self._tree.__hash__()
