import streamlit as st
import sympy
from utils.helpers import parse_expression, display_results, default_symbols
from utils.plotting_helpers import plot_function

st.set_page_config(page_title="Functions & Algebra", layout="wide")
st.title("📈 Functions & Algebra")

# --- Function Plotter ---
st.header("Function Plotter")
func_str_alg = st.text_input("Enter Function (e.g., 'x^3 - 2*x + 1', 'log(x, 10)', 'exp(-x^2)')", "x^2", key="alg_func")
var_str_alg = st.text_input("Variable", "x", key="alg_var")

plot_cols = st.columns(2)
with plot_cols[0]:
    plot_min_alg = st.number_input("Plot Min X", -10.0, key="alg_min")
with plot_cols[1]:
    plot_max_alg = st.number_input("Plot Max X", 10.0, key="alg_max")


if st.button("Plot Function", key="alg_plot_btn"):
    fig_alg, err_alg = plot_function(func_str_alg, var_str_alg, plot_min_alg, plot_max_alg)
    if err_alg:
        st.error(err_alg)
    else:
        st.plotly_chart(fig_alg, use_container_width=True)

    # TODO: Add analysis like finding roots (sympy.solve(expr, var)), domain/range (hard).

st.divider()

# --- Log & Exponential Tools ---
st.header("Logarithm & Exponential Tools")
log_exp_str = st.text_input("Enter Log/Exp Expression (e.g., 'log(x*y)', 'exp(a+b)', 'ln(x^2)')", "log(a**3)", key="log_exp_input")

op_cols = st.columns(3)
with op_cols[0]:
    if st.button("Expand Log", key="log_expand"):
        expr = parse_expression(log_exp_str)
        if expr:
            try:
                # Assume variables are positive for log expansion rules
                expanded_expr = sympy.expand_log(expr, force=True)
                display_results(expr, expanded_expr, "Log Expanded")
            except Exception as e:
                st.error(f"Could not expand log: {e}")

with op_cols[1]:
     if st.button("Combine Logs", key="log_combine"):
         expr = parse_expression(log_exp_str)
         if expr:
             try:
                 combined_expr = sympy.logcombine(expr, force=True)
                 display_results(expr, combined_expr, "Log Combined")
             except Exception as e:
                 st.error(f"Could not combine log: {e}")

with op_cols[2]:
     if st.button("Expand Exp", key="exp_expand"):
         expr = parse_expression(log_exp_str)
         if expr:
             try:
                 expanded_expr = sympy.expand(expr, func=True, power_exp=True) # More general expand might work
                 if expanded_expr == expr: # If general expand didn't change it, try specific exp expand
                     expanded_expr = sympy.expand(sympy.expand_power_exp(expr))
                 display_results(expr, expanded_expr, "Expanded")
             except Exception as e:
                 st.error(f"Could not expand: {e}")

# TODO: Add equation solving for log/exp equations.