import streamlit as st
import sympy
from .helpers import parse_expression, x, y, z, t, theta # Import default symbols and parser

def compute_limit(expr_str: str, var_str: str, point_str: str, dir_str='+'):
    """Computes the limit of an expression."""
    expr = parse_expression(expr_str)
    if expr is None: return None, "Parsing Error"

    try:
        var = sympy.symbols(var_str)
        # Try converting point to number, handle infinity
        if point_str.lower() in ['inf', 'infinity', 'oo']:
            point = sympy.oo
        elif point_str.lower() in ['-inf', '-infinity', '-oo']:
            point = -sympy.oo
        else:
            point = sympy.sympify(point_str) # Allows for numbers or symbolic points

        limit_val = sympy.limit(expr, var, point, dir=dir_str)
        return limit_val, None
    except Exception as e:
        return None, f"Could not compute limit: {e}"

def compute_derivative(expr_str: str, var_str: str, order: int = 1):
    """Computes the derivative of an expression."""
    expr = parse_expression(expr_str)
    if expr is None: return None, "Parsing Error"

    try:
        var = sympy.symbols(var_str)
        if order < 1:
            return None, "Order must be a positive integer."
        derivative_val = sympy.diff(expr, var, order)
        return derivative_val, None
    except Exception as e:
        return None, f"Could not compute derivative: {e}"

def compute_integral(expr_str: str, var_str: str, lower_bound_str=None, upper_bound_str=None):
    """Computes definite or indefinite integrals."""
    expr = parse_expression(expr_str)
    if expr is None: return None, "Parsing Error"

    try:
        var = sympy.symbols(var_str)

        if lower_bound_str is None and upper_bound_str is None:
            # Indefinite Integral
            integral_val = sympy.integrate(expr, var)
            return integral_val, None
        else:
            # Definite Integral
            # Try converting bounds to numbers, handle infinity
            def parse_bound(bound_str):
                 if bound_str.lower() in ['inf', 'infinity', 'oo']: return sympy.oo
                 if bound_str.lower() in ['-inf', '-infinity', '-oo']: return -sympy.oo
                 try:
                     return sympy.sympify(bound_str)
                 except (SyntaxError, TypeError, ValueError):
                     raise ValueError(f"Invalid bound: {bound_str}")

            lower = parse_bound(lower_bound_str)
            upper = parse_bound(upper_bound_str)

            integral_val = sympy.integrate(expr, (var, lower, upper))
            return integral_val, None

    except ValueError as e: # Catch invalid bounds specifically
        return None, str(e)
    except Exception as e:
        return None, f"Could not compute integral: {e}"


def compute_taylor_series(expr_str: str, var_str: str, point_str: str, order: int):
    """Computes the Taylor series expansion."""
    expr = parse_expression(expr_str)
    if expr is None: return None, "Parsing Error"

    try:
        var = sympy.symbols(var_str)
        point = sympy.sympify(point_str)
        if order < 0:
             return None, "Order cannot be negative."

        # Use .series() method
        # n=None gives O(x**6) by default, n=order gives up to that order term
        # series needs n = order+1 to get terms up to x^order
        taylor_val = expr.series(var, x0=point, n=order + 1) # .removeO() removes the O(...) term

        return taylor_val, None
    except Exception as e:
        return None, f"Could not compute Taylor series: {e}"

# TODO: Add helpers for sequence plotting, series convergence tests: