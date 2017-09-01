import ast
import inspect
import json
import types

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

        if self._tree["type"] == "unary":
            if self._tree["operator"]["type"] == "unknown":
                if self._tree["operator"]["value"] == "<class 'JsonExpressionTrees.JsonExpressionTree'>":
                    self._tree = self._tree["operand"]

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

        if isinstance(node, types.FunctionType):
            return JsonExpressionTree.visit(ast.parse(inspect.getsource(node)))

        if isinstance(node, ast.Module):
            return JsonExpressionTree.visit(node.body[0])

        if isinstance(node, ast.Lambda):
            return JsonExpressionTree.visit(node.body)

        if isinstance(node, ast.FunctionDef):
            return JsonExpressionTree.visit(node.body[0].value)

        if isinstance(node, ast.Return):
            return JsonExpressionTree.visit(node.value)

        if isinstance(node, int) or isinstance(node, float):
            return JsonExpressionTree._constant_node(node)

        if isinstance(node, ast.Num):
            return JsonExpressionTree._constant_node(node.n)

        if isinstance(node, ast.Assign):
            return JsonExpressionTree.visit(node.value)

        if isinstance(node, ast.Name):
            for frameInfo in inspect.stack():
                frameMembers = inspect.getmembers(frameInfo.frame)

                frameLocals = next(filter(lambda x: x[0] is "f_locals", frameMembers), None)[1]

                if node.id in frameLocals:
                    return JsonExpressionTree.visit(frameLocals[node.id])

                frameGlobals = next(filter(lambda x: x[0] is "f_globals", frameMembers), None)[1]

                if node.id in frameGlobals:
                    return JsonExpressionTree.visit(frameGlobals[node.id])

                frameBuiltIns = next(filter(lambda x: x[0] is "f_builtins", frameMembers), None)[1]

                if node.id in frameBuiltIns:
                    return JsonExpressionTree.visit(frameBuiltIns[node.id])

            return JsonExpressionTree._parameter_node(node.id)

        if isinstance(node, ast.UnaryOp):
            return JsonExpressionTree._unary_node(
                JsonExpressionTree.visit(node.op),
                JsonExpressionTree.visit(node.operand))

        if isinstance(node, ast.BinOp):
            return JsonExpressionTree._binary_node(
                JsonExpressionTree.visit(node.op),
                JsonExpressionTree.visit(node.left),
                JsonExpressionTree.visit(node.right))

        if isinstance(node, ast.Call):
            if len(node.args) == 1:
                return JsonExpressionTree._unary_node(
                    JsonExpressionTree.visit(node.func),
                    JsonExpressionTree.visit(node.args[0]))

            elif len(node.args) == 2:
                return JsonExpressionTree._binary_node(
                    JsonExpressionTree.visit(node.func),
                    JsonExpressionTree.visit(node.args[0]),
                    JsonExpressionTree.visit(node.args[1]))

        if isinstance(node, ast.Add):
            return JsonExpressionTree._operator_node("Add")

        if isinstance(node, ast.Pow):
            return JsonExpressionTree._operator_node("Pow")

        if repr(node) == "<built-in function abs>":
            return JsonExpressionTree._operator_node("Abs")

        return JsonExpressionTree._unknown_node(repr(node))

    @staticmethod
    def _unary_node(operator: dict, operand: dict) -> dict:

        if operator is None:
            raise TypeError

        if operand is None:
            raise TypeError

        return {
            "type": "unary",
            "operator": operator,
            "operand": operand
        }

    @staticmethod
    def _binary_node(operator: dict, operand_left: dict, operand_right: dict) -> dict:

        if operator is None:
            raise TypeError

        if operand_left is None:
            raise TypeError

        if operand_right is None:
            raise TypeError

        return {
            "type": "binary",
            "operator": operator,
            "operand_left": operand_left,
            "operand_right": operand_right
        }

    @staticmethod
    def _operator_node(value: str) -> dict:
        return {
            "type": "operator",
            "value": value
        }

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
            "value": name
        }

    @staticmethod
    def _unknown_node(unknown: object) -> dict:

        if unknown is None:
            raise TypeError

        return {
            "type": "unknown",
            "value": unknown
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
