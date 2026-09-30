import ast
import math
import operator


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _evaluate(node: ast.AST):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        result = node.value
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        result = _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    elif isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent magnitude must not exceed 100.")
        result = _BINARY_OPERATORS[type(node.op)](left, right)
    else:
        raise ValueError("Only basic arithmetic expressions are supported.")

    if isinstance(result, float) and not math.isfinite(result):
        raise ValueError("The result is outside the supported numeric range.")
    if isinstance(result, int) and result.bit_length() > 4096:
        raise ValueError("The result is outside the supported numeric range.")
    return result


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression without executing Python code."""
    try:
        if len(expression) > 256:
            raise ValueError("Expression is too long.")
        parsed = ast.parse(expression, mode="eval")
        return str(_evaluate(parsed.body))
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
        return f"Error: {error}"