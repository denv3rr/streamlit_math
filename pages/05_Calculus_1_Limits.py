import streamlit as st
import sympy
import numpy as np
import plotly.graph_objects as go
from utils.helpers import parse_expression, display_results, default_symbols, x, t, theta
from utils.calculus_helpers import compute_limit, compute_derivative
from utils.plotting_helpers import plot_function

st.set_page_config(page_title="Limits & Derivatives", layout="wide")
st.title("Σ Calculus 1: Limits & Derivatives")

# --- Limit Calculator ---
st.header("Limit Calculator")
lim_cols = st.columns([3, 1, 1, 1]) # Expression, Variable, Point, Direction
with lim_cols[0]:
    lim_expr_str = st.text_input("Expression", "sin(x)/x", key="lim_expr")
with lim_cols[1]:
    lim_var_str = st.text_input("Variable", "x", key="lim_var", max_chars=5)
with lim_cols[2]:
    lim_point_str = st.text_input("Point (e.g., 0, inf, -inf)", "0", key="lim_point")
with lim_cols[3]:
    lim_dir = st.selectbox("Direction", ['+', '-', 'two-sided'], index=2, key="lim_dir")

if st.button("Compute Limit", key="lim_compute"):
    sympy_dir = lim_dir if lim_dir != 'two-sided' else '+' # Sympy '+' for two-sided if point is finite

    limit_val, err = compute_limit(lim_expr_str, lim_var_str, lim_point_str, dir_str=lim_dir)

    if err:
        st.error(err)
    else:
        original_expr = parse_expression(lim_expr_str)
        st.write("---")
        st.write(f"**Limit of:**")
        st.latex(sympy.latex(original_expr))
        st.write(f"**As {lim_var_str} → {lim_point_str} ({'from ' + ('right' if lim_dir == '+' else 'left') if lim_dir != 'two-sided' else 'two-sided'}):**")
        st.latex(sympy.latex(limit_val))

st.divider()

# --- Derivative Calculator ---
st.header("Derivative Calculator & Tangent Line")
deriv_cols = st.columns([3, 1, 1]) # Expression, Variable, Order
with deriv_cols[0]:
    deriv_expr_str = st.text_input("Function f(x)", "x**3 * sin(x)", key="deriv_func")
with deriv_cols[1]:
    deriv_var_str = st.text_input("Variable", "x", key="deriv_var2", max_chars=5) # Use different key
with deriv_cols[2]:
    deriv_order = st.number_input("Order", min_value=1, max_value=5, value=1, step=1, key="deriv_order")

if st.button("Compute Derivative", key="deriv_compute"):
    derivative, err = compute_derivative(deriv_expr_str, deriv_var_str, deriv_order)
    if err:
        st.error(err)
    else:
        original_expr = parse_expression(deriv_expr_str)
        st.write("---")
        st.write(f"**Original Function $f({deriv_var_str})$:**")
        st.latex(sympy.latex(original_expr))
        st.write(f"**Derivative (Order {deriv_order}) $\\frac{{d^{deriv_order}}}{{d{deriv_var_str}^{deriv_order}}} f({deriv_var_str})$:**")
        st.latex(sympy.latex(derivative))

st.subheader("Visualize Tangent Line (Order 1)")
tan_cols = st.columns([3, 1, 2]) # Use function from above, Variable from above, Point
with tan_cols[0]:
    st.write(f"Using Function: `{deriv_expr_str}`")
    st.write(f"Using Variable: `{deriv_var_str}`")
with tan_cols[1]:
     tan_point_str = st.text_input("Point x₀", "pi/2", key="tan_point")
with tan_cols[2]:
     plot_range_tan = st.slider("Plot Range Width around x₀", 0.5, 20.0, 5.0, key="tan_range")


if st.button("Plot Function and Tangent Line", key="tan_plot"):
     original_expr = parse_expression(deriv_expr_str)
     if original_expr is not None and deriv_order == 1:
         try:
             var_sym = sympy.symbols(deriv_var_str)
             point_sym = parse_expression(tan_point_str) # Use parser to handle pi etc.
             point_val = point_sym.evalf()

             if not isinstance(point_val, (int, float, sympy.Float, sympy.Integer)):
                  st.error(f"Cannot evaluate tangent point '{tan_point_str}' to a number.")
             else:
                 point_val = float(point_val) # Ensure float for numpy/plotly
                 # Calculate derivative (order 1)
                 deriv_expr, err_deriv = compute_derivative(deriv_expr_str, deriv_var_str, 1)
                 if err_deriv:
                      st.error(f"Could not compute derivative for tangent line: {err_deriv}")
                 else:
                     # Calculate slope m = f'(x₀)
                     slope = deriv_expr.evalf(subs={var_sym: point_val})
                     if not isinstance(slope, (int, float, sympy.Float, sympy.Integer)):
                          st.error(f"Could not evaluate slope at x₀ = {point_val:.3f}. Is the function differentiable there?")
                     else:
                         slope = float(slope)
                         # Calculate y-coordinate y₀ = f(x₀)
                         y0 = original_expr.evalf(subs={var_sym: point_val})
                         y0 = float(y0)

                         # Tangent line equation: y - y₀ = m(x - x₀) => y = m(x - x₀) + y₀
                         tangent_expr_str = f"{slope} * ({deriv_var_str} - {point_val}) + {y0}"
                         tangent_expr_sym = parse_expression(tangent_expr_str)

                         st.write("---")
                         st.write(f"**At point $x_0 = {tan_point_str} \\approx {point_val:.4f}$:**")
                         st.latex(f"f(x_0) \\approx {y0:.4f}")
                         st.latex(f"f'(x_0) = \\text{{Slope }} m \\approx {slope:.4f}")
                         st.write("**Tangent Line Equation:**")
                         st.latex(f"y = {sympy.latex(tangent_expr_sym)}")

                         # Plotting
                         plot_min = point_val - plot_range_tan / 2
                         plot_max = point_val + plot_range_tan / 2

                         fig_main, err_main = plot_function(deriv_expr_str, deriv_var_str, plot_min, plot_max)
                         fig_tan, err_tan = plot_function(tangent_expr_str, deriv_var_str, plot_min, plot_max)

                         if err_main or err_tan:
                              st.error(f"Plotting Error: Main: {err_main}, Tangent: {err_tan}")
                         else:
                              # Combine plots
                              fig_combined = go.Figure(data=fig_main.data + fig_tan.data)
                              # Add point of tangency
                              fig_combined.add_trace(go.Scatter(x=[point_val], y=[y0], mode='markers', marker=dict(color='red', size=10), name='Point of Tangency'))

                              fig_combined.update_layout(
                                   title=f"Function $f({deriv_var_str})$ and Tangent Line at $x_0 \\approx {point_val:.3f}$",
                                   xaxis_title=f"${deriv_var_str}$",
                                   yaxis_title="y",
                                   legend_title="Trace"
                              )
                              st.plotly_chart(fig_combined, use_container_width=True)

         except Exception as e:
             st.error(f"An error occurred during tangent line visualization: {e}")
     elif deriv_order != 1:
         st.warning("Tangent line visualization is only available for order 1 derivatives.")
     else:
         st.error("Could not parse the original function.")