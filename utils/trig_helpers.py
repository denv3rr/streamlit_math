import sympy
import numpy as np
import math

# Define reference angles in radians and their exact SymPy values
# Using SymPy values ensures precision for comparisons and display
pi = sympy.pi
sqrt2 = sympy.sqrt(2)
sqrt3 = sympy.sqrt(3)

REFERENCE_ANGLES = {
    0: {'rad': 0, 'cos': 1, 'sin': 0},
    30: {'rad': pi/6, 'cos': sqrt3/2, 'sin': 1/2},
    45: {'rad': pi/4, 'cos': sqrt2/2, 'sin': sqrt2/2},
    60: {'rad': pi/3, 'cos': 1/2, 'sin': sqrt3/2},
    90: {'rad': pi/2, 'cos': 0, 'sin': 1},
    120: {'rad': 2*pi/3, 'cos': -1/2, 'sin': sqrt3/2},
    135: {'rad': 3*pi/4, 'cos': -sqrt2/2, 'sin': sqrt2/2},
    150: {'rad': 5*pi/6, 'cos': -sqrt3/2, 'sin': 1/2},
    180: {'rad': pi, 'cos': -1, 'sin': 0},
    210: {'rad': 7*pi/6, 'cos': -sqrt3/2, 'sin': -1/2},
    225: {'rad': 5*pi/4, 'cos': -sqrt2/2, 'sin': -sqrt2/2},
    240: {'rad': 4*pi/3, 'cos': -1/2, 'sin': -sqrt3/2},
    270: {'rad': 3*pi/2, 'cos': 0, 'sin': -1},
    300: {'rad': 5*pi/3, 'cos': 1/2, 'sin': -sqrt3/2},
    315: {'rad': 7*pi/4, 'cos': sqrt2/2, 'sin': -sqrt2/2},
    330: {'rad': 11*pi/6, 'cos': sqrt3/2, 'sin': -1/2},
    360: {'rad': 2*pi, 'cos': 1, 'sin': 0}, # Same as 0
}

# Common Trig Identities (can be expanded)
# Store as tuples: (Name, LHS_expression, RHS_expression) using SymPy expressions
# Use theta for consistency
theta = sympy.symbols('theta')
alpha, beta = sympy.symbols('alpha beta')

TRIG_IDENTITIES = [
    ("Pythagorean", sympy.sin(theta)**2 + sympy.cos(theta)**2, 1),
    ("Tan Definition", sympy.tan(theta), sympy.sin(theta)/sympy.cos(theta)),
    ("Sec Definition", sympy.sec(theta), 1/sympy.cos(theta)),
    ("Csc Definition", sympy.csc(theta), 1/sympy.sin(theta)),
    ("Cot Definition", sympy.cot(theta), sympy.cos(theta)/sympy.sin(theta)),
    ("Sum Angle Sin", sympy.sin(alpha + beta), sympy.sin(alpha)*sympy.cos(beta) + sympy.cos(alpha)*sympy.sin(beta)),
    ("Sum Angle Cos", sympy.cos(alpha + beta), sympy.cos(alpha)*sympy.cos(beta) - sympy.sin(alpha)*sympy.sin(beta)),
    ("Double Angle Sin", sympy.sin(2*theta), 2*sympy.sin(theta)*sympy.cos(theta)),
    ("Double Angle Cos", sympy.cos(2*theta), sympy.cos(theta)**2 - sympy.sin(theta)**2),
    # Add identities:
    # NEEDED: difference angles, half-angles, power-reducing, sum-to-product, ...
]

def get_trig_values(angle_rad_sympy):
    """Calculates all 6 trig values using SymPy for precision."""
    vals = {
        'sin': sympy.sin(angle_rad_sympy),
        'cos': sympy.cos(angle_rad_sympy),
        'tan': sympy.tan(angle_rad_sympy),
        'csc': sympy.csc(angle_rad_sympy),
        'sec': sympy.sec(angle_rad_sympy),
        'cot': sympy.cot(angle_rad_sympy),
    }
    # Evaluate numerically for display if needed, keep symbolic too
    vals_evalf = {k: v.evalf(5) if hasattr(v, 'evalf') else v for k, v in vals.items()}
    return vals, vals_evalf

def check_reference_angle(angle_deg):
    """Checks if the angle (in degrees) is a common reference angle."""
    for deg, data in REFERENCE_ANGLES.items():
        # Use tolerance for potential floating point inaccuracies if comparing rads
        # Comparing degrees is usually safer if input is degrees
        if math.isclose(angle_deg % 360, deg % 360) or \
           (deg == 360 and math.isclose(angle_deg % 360, 0)): # Handle 0/360 equivalence
             return deg, data
    return None, None