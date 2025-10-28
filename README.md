# calculator_app

A tiny Python CLI calculator with a safe AST-based evaluator and unit tests.

Features
- Supports +, -, *, /, %, **, parentheses and decimals.
- Interprets "50%" as 0.5 (basic percent shorthand).
- Comes with a minimal REPL and pytest tests.

Quickstart

1. Create a virtual environment (optional but recommended)
   python3 -m venv .venv
   source .venv/bin/activate

2. Install test deps (if needed)
   pip install pytest

3. Run the REPL
   python calculator.py

4. Run tests
   pytest

Notes on safety
- The evaluator parses and evaluates only a restricted set of AST nodes. No names,
  attribute access, or function calls are allowed. This reduces the risk of arbitrary code execution.
