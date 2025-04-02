import plotly.graph_objects as go
import numpy as np
import sympy
import math
from .helpers import parse_expression, default_symbols # Import parser and default symbols

def plot_function(expr_str: str, var_str: str = 'x', min_val: float = -10, max_val: float = 10, points: int = 500):
    """Plots a 1-variable function using Plotly."""
    expr = parse_expression(expr_str)
    if expr is None:
        return go.Figure(), "Parsing Error: Could not parse the function."

    try:
        var = sympy.symbols(var_str)
        # Check if the expression actually contains the variable
        if var not in expr.free_symbols:
             # Handle constant functions
             if expr.is_number:
                  y_vals = np.full(points, float(expr))
                  x_vals = np.linspace(min_val, max_val, points)
             else:
                return go.Figure(), f"Expression '{expr}' does not seem to depend on variable '{var}'."
        else:
             # Lambdify the expression for numerical evaluation
             func = sympy.lambdify(var, expr, modules=['numpy'])

             # Generate x values
             x_vals = np.linspace(min_val, max_val, points)

             # Evaluate the function, handle potential discontinuities carefully
             # Use complex type to potentially catch issues during evaluation (like sqrt(-1))
             y_vals_complex = func(x_vals.astype(np.complex128))

             # Filter out complex results if we expect real output, set them to NaN
             y_vals = np.real(y_vals_complex)
             y_vals[np.iscomplex(y_vals_complex)] = np.nan # Show gaps where function is complex

             # Handle infinities by replacing with NaN
             y_vals[np.isinf(y_vals)] = np.nan


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'f({var_str}) = {sympy.latex(expr)}'))

        fig.update_layout(
            title=f"Plot of ${sympy.latex(expr)}$",
            xaxis_title=f"${var_str}$",
            yaxis_title=f"$f({var_str})$",
            legend_title="Function"
        )
        return fig, None # Return figure and no error message

    except Exception as e:
        return go.Figure(), f"Could not plot function: {e}"


def plot_unit_circle(angle_rad_float=None, highlight_ref_angle=None):
    """Creates an interactive Plotly figure for the unit circle."""
    fig = go.Figure()

    # Draw the circle
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=-1, y0=-1, x1=1, y1=1,
                  line_color="LightSkyBlue", fillcolor="rgba(0,0,0,0)") # Transparent fill

    # Draw axes
    fig.add_shape(type="line", x0=-1.2, y0=0, x1=1.2, y1=0, line=dict(color="gray", width=1))
    fig.add_shape(type="line", x0=0, y0=-1.2, x1=0, y1=1.2, line=dict(color="gray", width=1))

    # Add annotations for axes labels
    fig.add_annotation(x=1.25, y=0, text="cos θ", showarrow=False)
    fig.add_annotation(x=0, y=1.25, text="sin θ", showarrow=False)
    fig.add_annotation(x=0, y=0, text="(0,0)", showarrow=False, yshift=10)

    # Add ticks (could be improved)
    for i in [-1, 1]:
        fig.add_shape(type="line", x0=i, y0=-0.05, x1=i, y1=0.05, line=dict(color="gray", width=1))
        fig.add_shape(type="line", x0=-0.05, y0=i, x1=0.05, y1=i, line=dict(color="gray", width=1))
        fig.add_annotation(x=i, y=-0.1, text=str(i), showarrow=False)
        fig.add_annotation(x=-0.1, y=i, text=str(i), showarrow=False, xshift=-5)


    if angle_rad_float is not None:
        # Calculate point on circle
        cos_val = math.cos(angle_rad_float)
        sin_val = math.sin(angle_rad_float)

        # Draw radius line
        fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines', line=dict(color='red', width=2), name='Radius'))

        # Draw point on circle
        fig.add_trace(go.Scatter(x=[cos_val], y=[sin_val], mode='markers', marker=dict(color='red', size=10), name=f'({cos_val:.3f}, {sin_val:.3f})'))

        # Draw associated right triangle
        fig.add_trace(go.Scatter(x=[0, cos_val, cos_val, 0], y=[0, 0, sin_val, 0], mode='lines', line=dict(color='orange', dash='dot'), name='Triangle'))
        # Add annotations for triangle sides if needed

    # Highlight reference angle point if specified
    if highlight_ref_angle is not None:
        ref_cos = float(highlight_ref_angle['cos'].evalf()) # Ensure float for plotting
        ref_sin = float(highlight_ref_angle['sin'].evalf())
        fig.add_trace(go.Scatter(x=[ref_cos], y=[ref_sin], mode='markers', marker=dict(color='green', size=12, symbol='star'), name='Reference Angle'))


    fig.update_layout(
        title="Interactive Unit Circle",
        xaxis=dict(range=[-1.5, 1.5], scaleratio=1), # Ensure aspect ratio is 1
        yaxis=dict(range=[-1.5, 1.5], scaleanchor="x"), # Link y scale to x scale
        showlegend=True,
        width=600, # Adjust size as needed
        height=600
    )
    return fig, None


def plot_solved_triangle(a, b, c, alpha, beta, gamma):
    """Plots the solved triangle using Plotly."""
    if not all(val is not None for val in [a, b, c, alpha, beta, gamma]):
        return go.Figure(), "Invalid input: Missing values for plotting."
    if not all(isinstance(val, (int, float)) for val in [a, b, c, alpha, beta, gamma]):
         return go.Figure(), "Invalid input: Values must be numeric for plotting."

    try:
        # Convert angles to radians for calculations
        alpha_rad = math.radians(alpha)
        beta_rad = math.radians(beta)
        # gamma_rad = math.radians(gamma) # Not directly needed for vertex placement

        # Place vertices
        A = (0, 0)
        C = (b, 0) # Place C along x-axis, side AC has length b
        # Calculate B using side c and angle alpha at A
        Bx = c * math.cos(alpha_rad)
        By = c * math.sin(alpha_rad)
        B = (Bx, By)

        # Verify calculated side 'a' (distance BC) as a sanity check
        calculated_a = math.sqrt((Bx - C[0])**2 + (By - C[1])**2)
        if not math.isclose(calculated_a, a, rel_tol=1e-5):
            # st.warning(f"Plotting Warning: Calculated side a ({calculated_a:.4f}) differs slightly from input/solved a ({a:.4f}). Plotting using calculated vertex B.")
            pass # Continue plotting, but maybe log this internally

        fig = go.Figure()

        # Draw sides
        fig.add_trace(go.Scatter(x=[A[0], B[0], C[0], A[0]], y=[A[1], B[1], C[1], A[1]],
                                 mode='lines+markers', name='Triangle Sides', line=dict(color='blue')))

        # Add annotations for vertices and side lengths
        mid_AB = ((A[0]+B[0])/2, (A[1]+B[1])/2)
        mid_BC = ((B[0]+C[0])/2, (B[1]+C[1])/2)
        mid_AC = ((A[0]+C[0])/2, (A[1]+C[1])/2)

        fig.add_annotation(x=A[0], y=A[1], text=f"A ({alpha:.1f}°)", showarrow=False, xshift=-10, yshift=-10)
        fig.add_annotation(x=B[0], y=B[1], text=f"B ({beta:.1f}°)", showarrow=False, xshift=0, yshift=10)
        fig.add_annotation(x=C[0], y=C[1], text=f"C ({gamma:.1f}°)", showarrow=False, xshift=10, yshift=-10)

        fig.add_annotation(x=mid_BC[0], y=mid_BC[1], text=f"a={a:.2f}", showarrow=False, bgcolor="rgba(255,255,255,0.7)")
        fig.add_annotation(x=mid_AC[0], y=mid_AC[1], text=f"b={b:.2f}", showarrow=False, bgcolor="rgba(255,255,255,0.7)")
        fig.add_annotation(x=mid_AB[0], y=mid_AB[1], text=f"c={c:.2f}", showarrow=False, bgcolor="rgba(255,255,255,0.7)")


        # Make aspect ratio equal
        fig.update_layout(
            title="Solved Triangle",
            xaxis=dict(scaleratio=1),
            yaxis=dict(scaleanchor="x"),
            showlegend=False
        )
        # Adjust axes ranges dynamically based on vertex coordinates
        all_x = [A[0], B[0], C[0]]
        all_y = [A[1], B[1], C[1]]
        x_range = [min(all_x) - abs(max(all_x)-min(all_x))*0.1 - 0.1, max(all_x) + abs(max(all_x)-min(all_x))*0.1 + 0.1] # Add padding
        y_range = [min(all_y) - abs(max(all_y)-min(all_y))*0.1 - 0.1, max(all_y) + abs(max(all_y)-min(all_y))*0.1 + 0.1]
        fig.update_xaxes(range=x_range)
        fig.update_yaxes(range=y_range)


        return fig, None
    except Exception as e:
        return go.Figure(), f"Could not plot triangle: {e}"


def plot_angle_elevation(distance, height, angle_deg):
    """Plots the angle of elevation scenario."""
    if not all(val is not None and isinstance(val, (int, float)) for val in [distance, height, angle_deg]):
        return go.Figure(), "Invalid numeric inputs for plotting."

    fig = go.Figure()

    # Ground line
    fig.add_trace(go.Scatter(x=[0, distance], y=[0, 0], mode='lines', name='Ground Distance', line=dict(color='brown')))
    # Object height
    fig.add_trace(go.Scatter(x=[distance, distance], y=[0, height], mode='lines', name='Object Height', line=dict(color='green')))
    # Line of sight
    fig.add_trace(go.Scatter(x=[0, distance], y=[0, height], mode='lines', name='Line of Sight', line=dict(color='blue', dash='dash')))

    # Angle arc (approximation using scatter points)
    arc_radius = min(distance, height) * 0.3 # Radius for arc
    angle_rad = math.radians(angle_deg)
    arc_angles = np.linspace(0, angle_rad, 20)
    arc_x = arc_radius * np.cos(arc_angles)
    arc_y = arc_radius * np.sin(arc_angles)
    fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color='red', width=1), name='Angle Arc'))

    # Annotations
    fig.add_annotation(x=distance/2, y=0, text=f"Dist={distance:.2f}", showarrow=False, yshift=-15)
    fig.add_annotation(x=distance, y=height/2, text=f"H={height:.2f}", showarrow=False, xshift=15)
    fig.add_annotation(x=arc_x[-1]*1.1, y=arc_y[-1]*1.1, text=f"{angle_deg:.1f}°", showarrow=False, bgcolor="rgba(255,255,255,0.5)")
    fig.add_annotation(x=0, y=0, text="Observer", showarrow=False, xshift=-10, yshift=-10)
    fig.add_annotation(x=distance, y=height, text="Object Top", showarrow=False, xshift=0, yshift=10)

    # Make aspect ratio equal and set ranges
    all_x = [0, distance]
    all_y = [0, height]
    x_range = [-0.1*distance, distance * 1.1]
    y_range = [-0.1*height, height * 1.1]

    fig.update_layout(
        title="Angle of Elevation/Depression",
        xaxis=dict(range=x_range, scaleratio=1),
        yaxis=dict(range=y_range, scaleanchor="x"),
        showlegend=True
    )
    return fig, None

# TODO: Add plotting functions for Bearings (still requires drawing compass lines / North reference)