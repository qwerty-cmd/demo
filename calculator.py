#!/usr/bin/env python3

"""
Simple CLI calculator with a safe evaluator using Python's AST.

Supports +, -, *, /, %, **, parentheses and unary +/-. Treats "50%" as 0.5
(using postfix % to mean percent). Does not allow names or function calls.
"""
import ast
import operator
import re
import readline  # optional: improves input UX on POSIX

# Mapping AST operator types to functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """Recursively evaluate an AST node composed only of allowed nodes."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.Num):  # fallback for older ast versions
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](_eval(node.operand))
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    # No Name, Call, Attribute, Subscript, etc. allowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate(expr: str):
    """
    Evaluate a math expression safely.
    - Supports +, -, *, /, %, **, parentheses and decimals.
    - Interprets '50%' as (50/100) => 0.5
    """
    if not isinstance(expr, str):
        raise TypeError("Expression must be a string")
    expr = expr.strip()
    if expr == "":
        raise ValueError("Empty expression")

    # Convert percent literals like 50% to (50/100)
    expr = re.sub(r'(\d+(\.\d+)?)\%', r'(\1/100)', expr)

    # Basic whitelist of characters (digits, operators, spaces, parentheses, dot)
    if not re.match(r'^[0-9+\-*/().%\s]+$', expr):
        raise ValueError("Expression contains invalid characters")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed)

def repl():
    print("Simple Calculator — type 'quit' or 'exit' or Ctrl-D to exit")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line or line.lower() in ("quit", "exit"):
            break
        try:
            result = evaluate(line)
            print(result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    repl()
