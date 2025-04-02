import streamlit as st
import numpy as np
import math
import sympy
import plotly.graph_objects as go
from utils.helpers import parse_expression, display_results, default_symbols, theta, alpha, beta
from utils.trig_helpers import REFERENCE_ANGLES, TRIG_IDENTITIES, get_trig_values, check_reference_angle
from utils.plotting_helpers import plot_unit_circle, plot_function

st.set_page_config(page_title="Trigonometry Workbench", layout="wide")
st.title("📐 Trigonometry Workbench")

# --- Interactive Unit Circle ---
st.header("Interactive Unit Circle")
col1, col2 = st.columns([1, 2]) # Input column, Plot column

with col1:
    unit_mode = st.radio("Angle Input Mode", ["Degrees", "Radians"], key="unit_mode")
    if unit_mode == "Degrees":
        angle_deg = st.slider("Angle (degrees)", 0.0, 360.0, 45.0, 1.0, key="angle_deg_slider")
        angle_rad_sympy = sympy.rad(angle_deg) # Keep symbolic for trig values
        angle_rad_float = math.radians(angle_deg) # Float for plotting
    else:
        # Allow direct input or slider for radians
        angle_rad_input = st.number_input("Angle (radians)", value=float(sympy.pi/4), min_value=0.0, max_value=float(2*sympy.pi), step=float(sympy.pi/12), format="%.4f", key="angle_rad_input")
        # Use a slider for easier exploration
        angle_rad_slider = st.slider("Angle (radians)", 0.0, float(2*sympy.pi), float(angle_rad_input), float(sympy.pi/36), format="%.4f", key="angle_rad_slider")
        angle_rad_sympy = angle_rad_slider # Keep symbolic/float
        angle_rad_float = float(angle_rad_slider) # Float for plotting
        angle_deg = math.degrees(angle_rad_float) # Calculate degrees for reference check

    st.write(f"Current Angle: {angle_deg:.2f}° = {angle_rad_float:.4f} radians")

    # Check if it's a reference angle
    ref_deg, ref_data = check_reference_angle(angle_deg)
    if ref_data:
        st.success(f"This is a common reference angle: {ref_deg}°")
        fig_unit, err_unit = plot_unit_circle(angle_rad_float, highlight_ref_angle=ref_data)
        vals_sym, vals_num = get_trig_values(ref_data['rad']) # Use exact rad value
    else:
        st.info("This is not a common reference angle.")
        fig_unit, err_unit = plot_unit_circle(angle_rad_float)
        vals_sym, vals_num = get_trig_values(angle_rad_sympy) # Use input angle

    # Display Trig Values
    st.subheader("Trigonometric Values:")
    if ref_data:
        st.write("(Using exact values for reference angle)")
    st.latex(f"\\sin({sympy.latex(angle_rad_sympy)}) = {sympy.latex(vals_sym['sin'])} \\approx {vals_num['sin']:.4f}")
    st.latex(f"\\cos({sympy.latex(angle_rad_sympy)}) = {sympy.latex(vals_sym['cos'])} \\approx {vals_num['cos']:.4f}")
    st.latex(f"\\tan({sympy.latex(angle_rad_sympy)}) = {sympy.latex(vals_sym['tan'])} \\approx {vals_num['tan']:.4f}")
    st.latex(f"\\csc({sympy.latex(angle_rad_sympy)}) = {sympy.latex(vals_sym['csc'])} \\approx {vals_num['csc']:.4f}")
    st.latex(f"\\sec({sympy.latex(angle_rad_sympy)}) = {sympy.latex(vals_sym['sec'])} \\approx {vals_num['sec']:.4f}")
    st.latex(f"\\cot({sympy.latex(angle_rad_sympy)}) = {sympy.latex(vals_sym['cot'])} \\approx {vals_num['cot']:.4f}")


with col2:
    if err_unit:
        st.error(err_unit)
    else:
        st.plotly_chart(fig_unit, use_container_width=True)

st.divider()

# --- Trig Function Grapher ---
st.header("Trigonometric Function Grapher")
func_options = ["sin(x)", "cos(x)", "tan(x)", "csc(x)", "sec(x)", "cot(x)", "a*sin(k*(x-p))+v", "a*cos(k*(x-p))+v"]
selected_func_base = st.selectbox("Select Function Type", func_options, index=0)

plot_range_min = st.number_input("Plot Range Min (x-axis)", value=-float(2*sympy.pi), format="%.2f")
plot_range_max = st.number_input("Plot Range Max (x-axis)", value=float(2*sympy.pi), format="%.2f")

if "sin" in selected_func_base or "cos" in selected_func_base:
     # Add sliders for parameters if a generic form is chosen
     if selected_func_base in ["a*sin(k*(x-p))+v", "a*cos(k*(x-p))+v"]:
        col_a, col_k, col_p, col_v = st.columns(4)
        with col_a:
             a_val = st.slider("Amplitude (a)", 0.1, 5.0, 1.0, 0.1)
        with col_k:
             k_val = st.slider("Frequency Factor (k)", 0.1, 5.0, 1.0, 0.1) # k relates to period P = 2pi/k
        with col_p:
             p_val = st.slider("Phase Shift (p)", -float(sympy.pi), float(sympy.pi), 0.0, float(sympy.pi/8), format="%.3f")
        with col_v:
             v_val = st.slider("Vertical Shift (v)", -3.0, 3.0, 0.0, 0.1)

        func_str = selected_func_base.replace('a', str(a_val)).replace('k', str(k_val)).replace('p', str(p_val)).replace('v', str(v_val))
        st.latex(f"f(x) = {sympy.latex(parse_expression(func_str))}")
     else:
         func_str = selected_func_base
else:
    func_str = selected_func_base

fig_func, err_func = plot_function(func_str, 'x', min_val=plot_range_min, max_val=plot_range_max)

if err_func:
    st.error(err_func)
elif fig_func:
    st.plotly_chart(fig_func, use_container_width=True)

st.divider()

# --- Identity Explorer & Verifier ---
st.header("Identity Explorer & Verifier")

col_id1, col_id2 = st.columns(2)

with col_id1:
    st.subheader("Explore Identities")
    identity_names = [name for name, _, _ in TRIG_IDENTITIES]
    selected_identity_name = st.selectbox("Select Identity", identity_names)
    selected_identity = next(id for id in TRIG_IDENTITIES if id[0] == selected_identity_name)
    st.write(f"**{selected_identity[0]}**")
    st.latex(f"{sympy.latex(selected_identity[1])} = {sympy.latex(selected_identity[2])}")
    # TODO: Add functionality to *apply* selected identity to a user expression

with col_id2:
    st.subheader("Verify Equivalence")
    expr1_str = st.text_input("Enter Expression 1", "sin(x)^2 + cos(x)^2", key="id_expr1")
    expr2_str = st.text_input("Enter Expression 2", "1", key="id_expr2")

    if st.button("Verify Equality"):
        expr1 = parse_expression(expr1_str)
        expr2 = parse_expression(expr2_str)

        if expr1 is not None and expr2 is not None:
            st.write("---")
            try:
                 # Method 1: Simplify difference
                 diff_simplified = sympy.simplify(expr1 - expr2)
                 st.write("Method 1: Simplify(Expression 1 - Expression 2)")
                 st.latex(f"Simplify({sympy.latex(expr1)} - ({sympy.latex(expr2)})) = {sympy.latex(diff_simplified)}")
                 if diff_simplified == 0:
                     st.success("Expressions ARE equivalent (difference simplifies to 0).")
                 else:
                     st.warning("Expressions might NOT be equivalent (difference did not simplify to 0).")

                 # Method 2: Trig simplification and equals()
                 st.write("---")
                 st.write("Method 2: TrigSimplify and .equals()")
                 expr1_trigsimp = sympy.trigsimp(expr1)
                 expr2_trigsimp = sympy.trigsimp(expr2)
                 st.latex(f"TrigSimp(Expr1) = {sympy.latex(expr1_trigsimp)}")
                 st.latex(f"TrigSimp(Expr2) = {sympy.latex(expr2_trigsimp)}")

                 if expr1_trigsimp.equals(expr2_trigsimp):
                     st.success("Expressions ARE equivalent (trig-simplified forms are equal).")
                 else:
                     # Check numerical equality over a range as a fallback test (not a proof)
                     try:
                         x_sym = default_symbols.get('x', sympy.symbols('x')) # Assume 'x' if present
                         if x_sym in expr1.free_symbols or x_sym in expr2.free_symbols:
                             # Check at a few points using evalf
                             are_numerically_close = True
                             for val in np.linspace(0.1, 2*np.pi - 0.1, 5): # Avoid poles if possible
                                 if not sympy.Abs(expr1.evalf(subs={x_sym: val}) - expr2.evalf(subs={x_sym: val})) < 1e-9:
                                     are_numerically_close = False
                                     break
                             if are_numerically_close:
                                  st.info("Expressions seem numerically equal over a test range, but symbolic proof failed.")
                             else:
                                 st.error("Expressions are NOT equivalent (symbolic forms differ, numerical check failed).")
                         else:
                              st.error("Expressions are NOT equivalent (symbolic forms differ).")

                     except Exception as e_eval:
                         st.warning(f"Could not perform numerical check: {e_eval}")
                         st.error("Expressions are likely NOT equivalent (symbolic forms differ).")


            except Exception as e:
                 st.error(f"An error occurred during verification: {e}")

st.divider()

# --- Equation Solver ---
st.header("Trigonometric Equation Solver")
eq_str = st.text_input("Enter Equation (e.g., 'sin(x) = 0.5', 'cos(2*theta) = sin(theta)')", "cos(x) = sqrt(3)/2")
var_str = st.text_input("Variable to solve for", "x")

if st.button("Solve Equation"):
     # Use solveset for potentially infinite solutions
     from sympy import solveset, S, Interval # S is Singleton, Interval for domains

     var = sympy.symbols(var_str)
     try:
         # Parse the equation string into a SymPy Eq object or expression = 0
         if '=' in eq_str:
             lhs_str, rhs_str = eq_str.split('=', 1)
             lhs = parse_expression(lhs_str.strip(), default_symbols)
             rhs = parse_expression(rhs_str.strip(), default_symbols)
             if lhs is None or rhs is None:
                 st.error("Could not parse one or both sides of the equation.")
             else:
                 equation = sympy.Eq(lhs, rhs)
                 # Define the domain (e.g., real numbers, or a specific interval like [0, 2*pi])
                 # Using Reals is common, but intervals can be more specific
                 # domain = S.Reals
                 domain = Interval(0, 2*sympy.pi) # Example: Solutions in [0, 2*pi]
                 st.write(f"Solving for {var} in the domain: ${sympy.latex(domain)}$")
                 solution = solveset(equation, var, domain=domain)
                 st.write("Solution Set:")
                 st.latex(sympy.latex(solution))
                 if not solution:
                     st.warning("No solution found in the specified domain.")

         else:
             # Assume expression = 0
             expr = parse_expression(eq_str.strip(), default_symbols)
             if expr is None:
                 st.error("Could not parse the expression.")
             else:
                domain = Interval(0, 2*sympy.pi) # Example: Solutions in [0, 2*pi]
                st.write(f"Solving {sympy.latex(expr)} = 0 for {var} in the domain: ${sympy.latex(domain)}$")
                solution = solveset(expr, var, domain=domain)
                st.write("Solution Set:")
                st.latex(sympy.latex(solution))
                if not solution:
                     st.warning("No solution found in the specified domain.")

     except Exception as e:
         st.error(f"Could not solve equation: {e}")