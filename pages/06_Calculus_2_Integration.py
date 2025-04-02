import streamlit as st
import sympy
import numpy as np
import plotly.graph_objects as go
from utils.helpers import parse_expression, display_results, default_symbols, x, t, theta
from utils.calculus_helpers import compute_integral
from utils.plotting_helpers import plot_function

st.set_page_config(page_title="Integration", layout="wide")
st.title("∫ Calculus 2: Integration")

# --- Indefinite Integral ---
st.header("Indefinite Integral Calculator")
int_cols1 = st.columns([3, 1])
with int_cols1[0]:
    indef_expr_str = st.text_input("Function f(x)", "cos(x)", key="indef_func")
with int_cols1[1]:
    indef_var_str = st.text_input("Variable", "x", key="indef_var", max_chars=5)

if st.button("Compute Indefinite Integral", key="indef_compute"):
    integral_val, err = compute_integral(indef_expr_str, indef_var_str)
    if err:
        st.error(err)
    else:
        original_expr = parse_expression(indef_expr_str)
        st.write("---")
        st.write(f"**Original Function $f({indef_var_str})$:**")
        st.latex(sympy.latex(original_expr))
        st.write(f"**Indefinite Integral $\\int f({indef_var_str}) \\, d{indef_var_str}$:**")
        st.latex(f"{sympy.latex(integral_val)} + C") # Remember the constant of integration!

st.divider()

# --- Definite Integral ---
st.header("Definite Integral Calculator & Visualization")
int_cols2 = st.columns([2, 1, 1, 1]) # Func, Var, Lower, Upper
with int_cols2[0]:
    def_expr_str = st.text_input("Function f(x)", "x**2", key="def_func")
with int_cols2[1]:
    def_var_str = st.text_input("Variable", "x", key="def_var", max_chars=5)
with int_cols2[2]:
    def_lower_str = st.text_input("Lower Bound a", "0", key="def_lower")
with int_cols2[3]:
    def_upper_str = st.text_input("Upper Bound b", "2", key="def_upper")

plot_def_integral = st.checkbox("Visualize Area under Curve", value=True, key="def_plot_check")

if st.button("Compute Definite Integral", key="def_compute"):
    integral_val, err = compute_integral(def_expr_str, def_var_str, def_lower_str, def_upper_str)

    if err:
        st.error(err)
    else:
        original_expr = parse_expression(def_expr_str)
        st.write("---")
        st.write(f"**Original Function $f({def_var_str})$:**")
        st.latex(sympy.latex(original_expr))
        st.write(f"**Definite Integral $\\int_{{{def_lower_str}}}^{{{def_upper_str}}} f({def_var_str}) \\, d{def_var_str}$:**")
        st.latex(sympy.latex(integral_val))
        try:
             st.write(f"**Numerical Value:** {integral_val.evalf():.6f}")
        except AttributeError:
             st.warning("Could not evaluate integral numerically (might be symbolic).")


        # Plotting
        if plot_def_integral:
            try:
                var_sym = sympy.symbols(def_var_str)
                lower_bound = parse_expression(def_lower_str).evalf()
                upper_bound = parse_expression(def_upper_str).evalf()
                lower_bound = float(lower_bound)
                upper_bound = float(upper_bound)

                if lower_bound >= upper_bound:
                    st.warning("Lower bound must be less than upper bound for standard area visualization.")
                else:
                    # Determine plot range (extend slightly beyond integration bounds)
                    padding = (upper_bound - lower_bound) * 0.2 + 0.5
                    plot_min = lower_bound - padding
                    plot_max = upper_bound + padding

                    fig_base, err_plot = plot_function(def_expr_str, def_var_str, plot_min, plot_max, points=500)

                    if err_plot:
                        st.error(f"Plotting Error: {err_plot}")
                    else:
                        # Add shaded region for integral area
                        # Generate points *within* the integration bounds for shading
                        x_fill = np.linspace(lower_bound, upper_bound, 200)
                        func_np = sympy.lambdify(var_sym, original_expr, modules=['numpy'])
                        y_fill_complex = func_np(x_fill.astype(np.complex128))
                        y_fill = np.real(y_fill_complex)
                        # Ensure no NaNs/Infs in fill data
                        valid_indices = ~np.isnan(y_fill) & ~np.isinf(y_fill)
                        x_fill = x_fill[valid_indices]
                        y_fill = y_fill[valid_indices]


                        fig_base.add_trace(go.Scatter(
                            x=np.concatenate([x_fill, x_fill[::-1]]), # x -> upper, x -> lower
                            y=np.concatenate([y_fill, np.zeros(len(y_fill))]), # y -> upper, 0 -> lower
                            fill='toself',
                            fillcolor='rgba(0,100,80,0.2)',
                            line=dict(color='rgba(255,255,255,0)'), # No border line for fill area
                            hoverinfo="skip",
                            showlegend=False,
                            name='Integral Area'
                        ))

                        fig_base.update_layout(
                             title=f"Area under $f({def_var_str}) = {sympy.latex(original_expr)}$ from {def_lower_str} to {def_upper_str}",
                             xaxis_title=f"${def_var_str}$",
                             yaxis_title=f"$f({def_var_str})$"
                        )
                        st.plotly_chart(fig_base, use_container_width=True)

            except Exception as e:
                 st.error(f"An error occurred during visualization: {e}")

# TODO: Add Integration Techniques section (more advanced)
# e.g., Show substitution steps, integration by parts setup.
st.divider()
st.info("More features soon: Integration technique exploration (Substitution, By Parts, etc.).")