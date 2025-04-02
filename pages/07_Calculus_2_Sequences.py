import streamlit as st
import sympy
import numpy as np
import plotly.graph_objects as go
from utils.helpers import parse_expression, display_results, default_symbols, x, t, theta
from utils.calculus_helpers import compute_taylor_series
from utils.plotting_helpers import plot_function

st.set_page_config(page_title="Sequences & Series", layout="wide")
st.title("♾️ Calculus 2: Sequences & Series")

n = sympy.symbols('n', integer=True, positive=True) # Common index variable

# --- Sequence Plotter ---
st.header("Sequence Plotter")
seq_cols = st.columns([3, 1, 1, 1])
with seq_cols[0]:
    seq_term_str = st.text_input("Sequence Term a_n", "1/n", key="seq_term")
with seq_cols[1]:
    # seq_var_str = st.text_input("Index Variable", "n", key="seq_var", max_chars=5)
    st.write("Index: n (integer, n ≥ 1)") # Assume index is n >= 1
    seq_var_sym = n
with seq_cols[2]:
    seq_n_min = 1 # Assume sequences start at n=1 for plotting ease
    seq_n_max = st.number_input("Max n", min_value=2, max_value=200, value=20, step=1, key="seq_nmax")

if st.button("Plot Sequence Terms", key="seq_plot"):
    seq_expr = parse_expression(seq_term_str, local_dict={str(seq_var_sym): seq_var_sym})
    if seq_expr is None:
        st.error("Could not parse sequence term.")
    else:
        try:
            n_values = np.arange(seq_n_min, seq_n_max + 1)
            # Evaluate the sequence term for each n
            # Need to substitute n and evaluate numerically
            terms = [seq_expr.subs({seq_var_sym: val}).evalf() for val in n_values]
            terms_float = [float(term) for term in terms] # Ensure numeric for plotting

            fig_seq = go.Figure()
            fig_seq.add_trace(go.Scatter(x=n_values, y=terms_float, mode='markers', name=f'$a_n = {sympy.latex(seq_expr)}$'))

            # Check limit as n -> oo (Divergence Test indicator)
            try:
                 seq_limit = sympy.limit(seq_expr, seq_var_sym, sympy.oo)
                 st.write("**Limit as n → ∞:**")
                 st.latex(f"\\lim_{{n \\to \\infty}} ({sympy.latex(seq_expr)}) = {sympy.latex(seq_limit)}")
                 if seq_limit != 0:
                     st.warning("Limit is non-zero. The corresponding series Σa_n diverges by the Divergence Test.")
                 else:
                     st.info("Limit is zero. The Divergence Test is inconclusive regarding the convergence of Σa_n.")
            except Exception as e_lim:
                 st.warning(f"Could not compute limit as n → ∞: {e_lim}")


            fig_seq.update_layout(
                title=f"Terms of the Sequence $a_n = {sympy.latex(seq_expr)}$",
                xaxis_title="n",
                yaxis_title="a_n",
                xaxis=dict(dtick=max(1, seq_n_max // 10)) # Adjust tick spacing
            )
            st.plotly_chart(fig_seq, use_container_width=True)

        except Exception as e:
            st.error(f"Could not compute or plot sequence terms: {e}")


st.divider()

# --- Taylor Series Explorer ---
st.header("Taylor Series Explorer")
taylor_cols = st.columns([2, 1, 1, 1]) # Func, Var, Point, Order
with taylor_cols[0]:
    taylor_expr_str = st.text_input("Function f(x)", "exp(x)", key="taylor_func")
with taylor_cols[1]:
    taylor_var_str = st.text_input("Variable", "x", key="taylor_var", max_chars=5)
with taylor_cols[2]:
    taylor_point_str = st.text_input("Center Point x₀", "0", key="taylor_point") # Maclaurin if 0
with taylor_cols[3]:
    taylor_order = st.number_input("Order", min_value=0, max_value=20, value=3, step=1, key="taylor_order")

plot_taylor = st.checkbox("Plot Function and Approximation", value=True, key="taylor_plot_check")
plot_range_taylor = st.slider("Plot Range Width around x₀", 0.5, 20.0, 6.0, key="taylor_range")

if st.button("Compute Taylor Series", key="taylor_compute"):
    series_val, err = compute_taylor_series(taylor_expr_str, taylor_var_str, taylor_point_str, taylor_order)

    if err:
        st.error(err)
    else:
        original_expr = parse_expression(taylor_expr_str)
        st.write("---")
        st.write(f"**Original Function $f({taylor_var_str})$:**")
        st.latex(sympy.latex(original_expr))
        st.write(f"**Taylor Polynomial (Order {taylor_order}) around ${taylor_var_str}={taylor_point_str}$:**")
        # Remove the O(...) term for polynomial display
        taylor_poly = series_val.removeO()
        st.latex(sympy.latex(taylor_poly))

        if plot_taylor:
            try:
                point_sym = parse_expression(taylor_point_str)
                point_val = float(point_sym.evalf())

                plot_min = point_val - plot_range_taylor / 2
                plot_max = point_val + plot_range_taylor / 2

                # Convert polynomial to string for plotting function
                taylor_poly_str = str(taylor_poly)

                fig_orig, err_orig = plot_function(taylor_expr_str, taylor_var_str, plot_min, plot_max)
                fig_taylor, err_taylor = plot_function(taylor_poly_str, taylor_var_str, plot_min, plot_max)

                if err_orig or err_taylor:
                    st.error(f"Plotting error: Original: {err_orig}, Taylor: {err_taylor}")
                else:
                    # Combine plots
                    fig_combined = go.Figure(data=fig_orig.data + fig_taylor.data)
                    # Update trace names
                    fig_combined.data[0].name = f'f({taylor_var_str})' # Original function
                    fig_combined.data[1].name = f'Taylor Order {taylor_order}' # Taylor Polynomial
                    fig_combined.data[1].line.dash = 'dash' # Dashed line for approximation

                    fig_combined.update_layout(
                         title=f"Function vs Taylor Approximation (Order {taylor_order})",
                         xaxis_title=f"${taylor_var_str}$",
                         yaxis_title="y",
                         legend_title="Trace"
                    )
                    st.plotly_chart(fig_combined, use_container_width=True)

            except Exception as e:
                 st.error(f"An error occurred during plotting: {e}")


st.divider()
# --- Series Convergence ---
st.header("Series Convergence (Basic Tests)")
conv_term_str = st.text_input("Series Term a_n (function of n)", "1/n**2", key="conv_term")

if st.button("Test Convergence", key="conv_test"):
     term_expr = parse_expression(conv_term_str, local_dict={'n': n}) # Use n as symbol
     if term_expr is None:
         st.error("Could not parse series term.")
     else:
         st.write(f"Testing convergence of $\\sum_{{n=1}}^{{\\infty}} ({sympy.latex(term_expr)})$")
         st.write("---")
         # 1. Divergence Test
         try:
             term_limit = sympy.limit(term_expr, n, sympy.oo)
             st.write("**1. Divergence Test:**")
             st.latex(f"\\lim_{{n \\to \\infty}} a_n = \\lim_{{n \\to \\infty}} ({sympy.latex(term_expr)}) = {sympy.latex(term_limit)}")
             if term_limit != 0:
                 st.error("Series Diverges (Limit is non-zero).")
                 # Stop testing if diverges
             else:
                 st.success("Limit is zero. Test is inconclusive. Proceeding...")
                 st.write("---")
                 # 2. Try SymPy's automatic summation (can be slow/fail)
                 st.write("**2. SymPy Summation Check (Experimental):**")
                 try:
                     # Try to compute the sum symbolically
                     inf_sum = sympy.summation(term_expr, (n, 1, sympy.oo))
                     st.write("Symbolic Sum Result:")
                     st.latex(sympy.latex(inf_sum))
                     if inf_sum.has(sympy.Sum) or inf_sum.has(sympy.oo) or inf_sum.has(sympy.zoo):
                          st.warning("SymPy could not find a finite symbolic sum.")
                          # Check convergence attribute if sum failed
                          is_conv = inf_sum.is_convergent()
                          st.write(f"SymPy's `is_convergent()` check: **{is_conv}**")
                          if is_conv == True:
                              st.success("SymPy suggests the series Converges.")
                          elif is_conv == False:
                              st.error("SymPy suggests the series Diverges.")
                          else:
                              st.info("SymPy convergence check inconclusive.")

                     elif inf_sum.is_finite:
                          st.success(f"Series Converges (Symbolic sum = {inf_sum.evalf():.6f}).")
                     else:
                          st.warning("Symbolic sum result is complex or not clearly finite/infinite.")
                          st.info("Try specific tests if applicable (not implemented automatically here).")

                 except Exception as e_sum:
                      st.warning(f"Could not compute symbolic sum or check convergence automatically: {e_sum}")
                      st.info("This often happens for complex series. Try specific tests if applicable.")

                 # TODO: Add buttons/logic for specific tests (Ratio, Root, Integral, Comparison)
                 st.write("---")
                 st.info("Further tests (Ratio, Root, Integral, Comparison) require specific implementation or manual application.")

         except Exception as e_lim:
              st.error(f"Could not compute limit for Divergence Test: {e_lim}")