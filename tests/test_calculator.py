import calculator
import math
import pytest

def test_basic_addition():
    assert calculator.evaluate("1+2") == 3

def test_precedence():
    assert calculator.evaluate("2+3*4") == 14

def test_parentheses():
    assert calculator.evaluate("(2+3)*4") == 20

def test_decimal():
    assert math.isclose(calculator.evaluate("0.5+0.25"), 0.75, rel_tol=1e-12)

def test_unary():
    assert calculator.evaluate("-3 + +5") == 2

def test_power_modulo():
    assert calculator.evaluate("2**3 + 5%") == pytest.approx(8 + 0.05)

def test_percent_literal():
    assert calculator.evaluate("50%") == 0.5
