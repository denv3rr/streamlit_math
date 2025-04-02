import streamlit as st
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Define common symbols
x, y, z, t, theta = sympy.symbols('x y z t theta')
a, b, c, k = sympy.symbols('a b c k') # Common constants or variables

# Add more symbols as needed
default_symbols = {
    'x': x, 'y': y, 'z': z, 't': t, 'theta': theta,
    'a': a, 'b': b, 'c': c, 'k': k,
    'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
    'csc': sympy.csc, 'sec': sympy.sec, 'cot': sympy.cot,
    'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
    'log': sympy.log, 'ln': sympy.ln, 'exp': sympy.exp,
    'sqrt': sympy.sqrt, 'pi': sympy.pi, 'e': sympy.E, 'I': sympy.I
}

def parse_expression(expr_str: str, local_dict=None):
    """
    Parses a string into a SymPy expression with error handling.
    Includes standard transformations and implicit multiplication.
    """
    if local_dict is None:
        local_dict = default_symbols

    transformations = standard_transformations + (implicit_multiplication_application,)

    if not expr_str:
        st.warning("Input expression cannot be empty.")
        return None
    try:
        # Safely parse the expression
        parsed_expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
        return parsed_expr
    except (SyntaxError, TypeError, ValueError, NameError) as e:
        st.error(f"Invalid expression: {e}")
        st.error(f"Please use standard mathematical notation (e.g., 'x^2 + sin(theta)', 'log(x, 10)', 'exp(a*t)'). Ensure all variables are defined or standard (x, y, z, t, theta, a, b, c, k).")
        return None
    except Exception as e:
        st.error(f"An unexpected parsing error occurred: {e}")
        return None

def display_results(original_expr, result_expr, operation_name="Result"):
    """Formats and displays original and resulting expressions."""
    st.write(f"**Original Expression:**")
    st.latex(sympy.latex(original_expr))
    st.write(f"**{operation_name}:**")
    if result_expr is not None:
        st.latex(sympy.latex(result_expr))
    else:
        st.warning("Calculation resulted in None.")

# Add helper functions here as needed: