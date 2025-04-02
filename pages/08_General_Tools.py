import streamlit as st
import sympy
from utils.helpers import parse_expression, display_results, default_symbols

st.set_page_config(page_title="General Math Tools", layout="wide")
st.title("🛠️ General Tools")

# --- Expression Simplifier ---
st.header("Expression Simplifier")
simp_expr_str = st.text_area("Enter Mathematical Expression", "(x**2 - 1) / (x - 1)", key="simp_expr_input")

st.write("Apply Simplification Function:")
simp_cols = st.columns(5)
simp_result = None
original_expr_parsed = None

if simp_expr_str:
    original_expr_parsed = parse_expression(simp_expr_str)

with simp_cols[0]:
    if st.button("Simplify", key="simp_gen"):
        if original_expr_parsed:
            simp_result = sympy.simplify(original_expr_parsed)
            op_name = "General Simplify"

with simp_cols[1]:
    if st.button("Expand", key="simp_exp"):
         if original_expr_parsed:
            simp_result = sympy.expand(original_expr_parsed)
            op_name = "Expand"

with simp_cols[2]:
    if st.button("Factor", key="simp_fac"):
         if original_expr_parsed:
            simp_result = sympy.factor(original_expr_parsed)
            op_name = "Factor"

with simp_cols[3]:
    if st.button("Trig Simplify", key="simp_trig"):
         if original_expr_parsed:
            simp_result = sympy.trigsimp(original_expr_parsed)
            op_name = "Trigonometric Simplify"

with simp_cols[4]:
    if st.button("Cancel", key="simp_can"):
         if original_expr_parsed:
            simp_result = sympy.cancel(original_expr_parsed)
            op_name = "Cancel Terms"

# Add more buttons if needed (powsimp, combsimp, etc.)

st.write("---")
if original_expr_parsed is None and simp_expr_str:
    st.error("Could not parse the input expression.")
elif simp_result is not None:
    display_results(original_expr_parsed, simp_result, op_name)
elif original_expr_parsed:
     st.write("**Original Expression:**")
     st.latex(sympy.latex(original_expr_parsed))
     st.info("Click a button above to apply a simplification.")
else:
    st.info("Enter an expression to simplify.")


st.divider()

# --- Equality Checker ---
st.header("Equality Checker")
eq_check_cols = st.columns(2)
with eq_check_cols[0]:
    eq_expr1_str = st.text_area("Expression 1", "cos(x)**2 - sin(x)**2", key="eq_expr1")
with eq_check_cols[1]:
    eq_expr2_str = st.text_area("Expression 2", "cos(2*x)", key="eq_expr2")

if st.button("Check if Expressions are Equal", key="eq_check_button"):
    expr1 = parse_expression(eq_expr1_str)
    expr2 = parse_expression(eq_expr2_str)

    if expr1 is not None and expr2 is not None:
        st.write("---")
        st.write("**Expression 1:**")
        st.latex(sympy.latex(expr1))
        st.write("**Expression 2:**")
        st.latex(sympy.latex(expr2))
        st.write("---")
        st.write("**Verification Methods:**")

        try:
            # Method 1: Simplify difference
            diff_simplified = sympy.simplify(expr1 - expr2)
            st.write("*Method 1: Simplify(Expression 1 - Expression 2)*")
            st.latex(f"\\rightarrow {sympy.latex(diff_simplified)}")
            if diff_simplified == 0:
                st.success("Result: Expressions ARE equivalent (difference simplifies to 0).")
            else:
                st.warning("Result: Expressions might NOT be equivalent (difference did not simplify to 0). Trying other methods...")

                # Method 2: Using .equals() which applies more transformations
                st.write("*Method 2: expr1.equals(expr2)*")
                are_equal = expr1.equals(expr2)
                st.write(f"Result: `{are_equal}`")
                if are_equal:
                     st.success("Result: Expressions ARE equivalent (using `.equals()` method).")
                else:
                     # Try simplifying both first
                     st.write("*Method 3: Simplify both and compare*")
                     expr1_s = sympy.simplify(expr1)
                     expr2_s = sympy.simplify(expr2)
                     st.latex(f"Simplify(Expr1) \\rightarrow {sympy.latex(expr1_s)}")
                     st.latex(f"Simplify(Expr2) \\rightarrow {sympy.latex(expr2_s)}")
                     if expr1_s.equals(expr2_s):
                          st.success("Result: Expressions ARE equivalent (simplified forms are equal).")
                     else:
                          st.error("Result: Expressions are LIKELY NOT equivalent (failed multiple checks).")

        except Exception as e:
            st.error(f"An error occurred during verification: {e}")

    elif not expr1:
        st.error("Could not parse Expression 1.")
    elif not expr2:
        st.error("Could not parse Expression 2.")