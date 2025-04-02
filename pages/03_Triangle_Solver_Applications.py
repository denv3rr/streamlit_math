import streamlit as st
import math
from utils.geometry_helpers import (solve_sss, solve_sas, solve_asa, solve_aas,
                                    solve_angle_elevation, solve_height_from_elevation)
from utils.plotting_helpers import plot_solved_triangle, plot_angle_elevation
import plotly.graph_objects as go

st.set_page_config(page_title="Triangle Solver & Applications", layout="wide")
st.title("🔺 Triangle Solver & Applications")

tab1, tab2 = st.tabs(["Triangle Solver", "Geometric Applications"])

# --- Triangle Solver Tab ---
with tab1:
    st.header("Solve Triangle")
    solve_type = st.selectbox("Given Information Type", ["SSS", "SAS", "ASA", "AAS"])

    col_inputs, col_results = st.columns(2)

    a, b, c = None, None, None
    alpha, beta, gamma = None, None, None # Angles opposite sides a, b, c respectively
    error_msg = None
    solved_values = {}

    with col_inputs:
        st.subheader("Inputs")
        if solve_type == "SSS":
            a = st.number_input("Side a", min_value=0.01, value=5.0, format="%.4f")
            b = st.number_input("Side b", min_value=0.01, value=6.0, format="%.4f")
            c = st.number_input("Side c", min_value=0.01, value=7.0, format="%.4f")
            if st.button(f"Solve {solve_type}"):
                 alpha, beta, gamma, error_msg = solve_sss(a, b, c)
                 if not error_msg: solved_values = {'α': alpha, 'β': beta, 'γ': gamma}

        elif solve_type == "SAS":
            b = st.number_input("Side b", min_value=0.01, value=6.0, format="%.4f")
            gamma = st.number_input("Angle γ (between a and b, degrees)", min_value=0.0, max_value=180.0, value=60.0, format="%.4f")
            a = st.number_input("Side a", min_value=0.01, value=7.0, format="%.4f")
            if st.button(f"Solve {solve_type}"):
                c, alpha, beta, error_msg = solve_sas(b, gamma, a)
                if not error_msg: solved_values = {'c': c, 'α': alpha, 'β': beta}

        elif solve_type == "ASA":
            beta = st.number_input("Angle β (degrees)", min_value=0.0, max_value=180.0, value=60.0, format="%.4f")
            c = st.number_input("Side c (between α and β)", min_value=0.01, value=7.0, format="%.4f")
            alpha = st.number_input("Angle α (degrees)", min_value=0.0, max_value=180.0, value=50.0, format="%.4f")
            if st.button(f"Solve {solve_type}"):
                 if alpha + beta >= 180:
                      error_msg = "Invalid input: Sum of angles α and β must be less than 180°."
                 else:
                    a, b, gamma, error_msg = solve_asa(beta, c, alpha)
                    if not error_msg: solved_values = {'a': a, 'b': b, 'γ': gamma}

        elif solve_type == "AAS":
            alpha = st.number_input("Angle α (degrees)", min_value=0.0, max_value=180.0, value=50.0, format="%.4f")
            beta = st.number_input("Angle β (degrees)", min_value=0.0, max_value=180.0, value=60.0, format="%.4f")
            a = st.number_input("Side a (opposite α)", min_value=0.01, value=6.0, format="%.4f")
            if st.button(f"Solve {solve_type}"):
                if alpha + beta >= 180:
                      error_msg = "Invalid input: Sum of angles α and β must be less than 180°."
                else:
                    b, c, gamma, error_msg = solve_aas(alpha, beta, a)
                    if not error_msg: solved_values = {'b': b, 'c': c, 'γ': gamma}

    with col_results:
        st.subheader("Results")
        if error_msg:
            st.error(error_msg)
        elif solved_values:
            st.success("Triangle Solved Successfully!")
            # Display all 6 values (inputs + solved)
            final_a = a if a is not None else solved_values.get('a')
            final_b = b if b is not None else solved_values.get('b')
            final_c = c if c is not None else solved_values.get('c')
            final_alpha = alpha if alpha is not None else solved_values.get('α')
            final_beta = beta if beta is not None else solved_values.get('β')
            final_gamma = gamma if gamma is not None else solved_values.get('γ')

            st.write(f"**Sides:** a = {final_a:.4f}, b = {final_b:.4f}, c = {final_c:.4f}")
            st.write(f"**Angles (degrees):** α = {final_alpha:.4f}°, β = {final_beta:.4f}°, γ = {final_gamma:.4f}°")

            # Plotting
            if all(v is not None for v in [final_a, final_b, final_c, final_alpha, final_beta, final_gamma]):
                 fig_tri, err_tri_plot = plot_solved_triangle(final_a, final_b, final_c, final_alpha, final_beta, final_gamma)
                 if err_tri_plot:
                     st.warning(f"Plotting Error: {err_tri_plot}")
                 else:
                     st.plotly_chart(fig_tri, use_container_width=True)
            else:
                 st.warning("Could not plot triangle: Missing values.")

        else:
            st.info("Enter triangle parameters and click 'Solve'.")

# --- Geometric Applications Tab ---
with tab2:
    st.header("Geometric Applications")
    app_type = st.selectbox("Select Application Type", ["Angle of Elevation/Depression"]) # TODO: Add Bearings

    app_col_inputs, app_col_results = st.columns(2)

    with app_col_inputs:
        st.subheader("Inputs")
        if app_type == "Angle of Elevation/Depression":
            solve_for = st.radio("Solve for:", ["Angle", "Height/Depth"])
            distance = st.number_input("Horizontal Distance", min_value=0.01, value=100.0)

            angle, height = None, None
            app_error_msg = None
            plot_fig = go.Figure()
            plot_err = "Enter values and solve."

            if solve_for == "Angle":
                height = st.number_input("Object Height (for Elevation) / Depth (for Depression)", value=50.0) # Allow negative for depression?
                if st.button("Calculate Angle"):
                    angle, app_error_msg = solve_angle_elevation(distance, height)
                    if not app_error_msg:
                         plot_fig, plot_err = plot_angle_elevation(distance, height, angle)

            elif solve_for == "Height/Depth":
                angle = st.number_input("Angle (degrees, 0-90)", min_value=0.1, max_value=89.9, value=30.0) # Use 0-90 for simplicity
                is_depression = st.checkbox("Is this an Angle of Depression?")
                if st.button("Calculate Height/Depth"):
                     height, app_error_msg = solve_height_from_elevation(distance, angle)
                     if not app_error_msg:
                          # Plotting depression often mirrors elevation, just interpret height as depth
                          plot_height = -height if is_depression else height
                          plot_fig, plot_err = plot_angle_elevation(distance, plot_height, angle)


    with app_col_results:
        st.subheader("Results")
        if app_error_msg:
             st.error(app_error_msg)
        elif solve_for == "Angle" and angle is not None:
             st.success(f"Calculated Angle = {angle:.4f}°")
             if plot_err: st.warning(f"Plotting issue: {plot_err}")
             else: st.plotly_chart(plot_fig, use_container_width=True)
        elif solve_for == "Height/Depth" and height is not None:
             label = "Depth" if is_depression else "Height"
             st.success(f"Calculated {label} = {height:.4f}")
             if plot_err: st.warning(f"Plotting issue: {plot_err}")
             else: st.plotly_chart(plot_fig, use_container_width=True)
        else:
             st.info("Enter parameters and click Calculate.")

        # TODO: Implement Bearing calculations and plotting
        if app_type == "Bearings":
            st.warning("Bearing calculations and plotting are not yet implemented.")