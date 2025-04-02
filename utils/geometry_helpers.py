import math
import numpy as np
import streamlit as st

# --- Triangle Solving Logic ---

def solve_sss(a, b, c):
    """Solves a triangle given three sides (SSS). Returns angles in degrees."""
    # Validate input
    if not (a + b > c and a + c > b and b + c > a):
        return None, None, None, "Invalid triangle: Sides violate triangle inequality."

    try:
        alpha = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
        beta = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
        gamma = 180 - alpha - beta # More stable than calculating the third angle via acos
        # Final check if angles sum close to 180
        if not math.isclose(alpha + beta + gamma, 180):
             # Fallback calculation for gamma
             gamma = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
             if not math.isclose(alpha + beta + gamma, 180):
                 return None, None, None, "Calculation error: angles do not sum to 180."

        return alpha, beta, gamma, None # angles opposite a, b, c
    except ValueError:
        # This can happen if the fraction in acos is slightly outside [-1, 1] due to float errors
         return None, None, None, "Calculation error: Invalid value for acos (likely floating point issue)."
    except Exception as e:
        return None, None, None, f"An unexpected error occurred: {e}"

def solve_sas(b, gamma_deg, a):
    """Solves a triangle given two sides and the included angle (SAS)."""
    # Validate input
    if not (a > 0 and b > 0 and 0 < gamma_deg < 180):
        return None, None, None, None, None, "Invalid input: Sides must be positive and angle between 0 and 180."

    try:
        gamma_rad = math.radians(gamma_deg)
        c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(gamma_rad)) # Law of Cosines

        # Law of Sines to find another angle (be careful with arcsin ambiguity)
        # It's safer to find the angle opposite the smaller side first OR use Law of Cosines again
        alpha = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
        beta = 180 - alpha - gamma_deg

        if not math.isclose(alpha + beta + gamma_deg, 180):
             beta = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c))) # Recalculate beta
             if not math.isclose(alpha + beta + gamma_deg, 180):
                 return None, None, None, None, None, "Calculation error: angles do not sum to 180."

        return c, alpha, beta, None # Solved side c, angle alpha (opp a), angle beta (opp b)
    except ValueError:
         return None, None, None, None, None, "Calculation error: Invalid value for acos (likely floating point issue)."
    except Exception as e:
        return None, None, None, None, None, f"An unexpected error occurred: {e}"

def solve_asa(beta_deg, c, alpha_deg):
    """Solves a triangle given two angles and the included side (ASA)."""
    # Validate input
    if not (c > 0 and 0 < alpha_deg < 180 and 0 < beta_deg < 180 and alpha_deg + beta_deg < 180):
        return None, None, None, None, None, "Invalid input: Side must be positive, angles between 0-180, and sum < 180."

    try:
        gamma_deg = 180 - alpha_deg - beta_deg
        alpha_rad = math.radians(alpha_deg)
        beta_rad = math.radians(beta_deg)
        gamma_rad = math.radians(gamma_deg)

        # Law of Sines
        a = c * (math.sin(alpha_rad) / math.sin(gamma_rad))
        b = c * (math.sin(beta_rad) / math.sin(gamma_rad))

        return a, b, gamma_deg, None # Solved sides a, b, angle gamma
    except Exception as e:
        return None, None, None, None, None, f"An unexpected error occurred: {e}"

def solve_aas(alpha_deg, beta_deg, a):
    """Solves a triangle given two angles and a non-included side (AAS)."""
     # Validate input
    if not (a > 0 and 0 < alpha_deg < 180 and 0 < beta_deg < 180 and alpha_deg + beta_deg < 180):
        return None, None, None, None, None, "Invalid input: Side must be positive, angles between 0-180, and sum < 180."

    try:
        gamma_deg = 180 - alpha_deg - beta_deg
        alpha_rad = math.radians(alpha_deg)
        beta_rad = math.radians(beta_deg)
        gamma_rad = math.radians(gamma_deg)

        # Law of Sines
        b = a * (math.sin(beta_rad) / math.sin(alpha_rad))
        c = a * (math.sin(gamma_rad) / math.sin(alpha_rad))

        return b, c, gamma_deg, None # Solved sides b, c, angle gamma
    except Exception as e:
        return None, None, None, None, None, f"An unexpected error occurred: {e}"


# --- Bearing Calculation Helper (Example) ---
def calculate_endpoint_from_bearing(start_lat, start_lon, bearing_deg, distance_km):
    """
    Calculates the end coordinates given start coordinates, bearing, and distance.
    Uses the Haversine formula principles.
    
    NOTE: For typical pre-calc problems NOT on a sphere, simpler plane trig is used.
          This is a placeholder for geographic bearings if needed later.
          For simple plane trig: dx = dist * sin(bearing_rad), dy = dist * cos(bearing_rad)
    """
    R = 6371 # Earth radius in km
    bearing_rad = math.radians(bearing_deg)
    lat1_rad = math.radians(start_lat)
    lon1_rad = math.radians(start_lon)
    d_R = distance_km / R # Angular distance

    lat2_rad = math.asin(math.sin(lat1_rad)*math.cos(d_R) +
                         math.cos(lat1_rad)*math.sin(d_R)*math.cos(bearing_rad))
    lon2_rad = lon1_rad + math.atan2(math.sin(bearing_rad)*math.sin(d_R)*math.cos(lat1_rad),
                                     math.cos(d_R)-math.sin(lat1_rad)*math.sin(lat2_rad))

    return math.degrees(lat2_rad), math.degrees(lon2_rad)

# --- Angle of Elevation/Depression Helper ---
def solve_angle_elevation(distance, height):
    """ Calculates angle of elevation given horizontal distance and height. """
    if distance <= 0: return None, "Distance must be positive."
    try:
        angle_rad = math.atan(height / distance)
        return math.degrees(angle_rad), None
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

def solve_height_from_elevation(distance, angle_deg):
    """ Calculates height given horizontal distance and angle of elevation. """
    if distance <= 0 or angle_deg <= 0 or angle_deg >= 90:
        return None, "Distance must be positive, angle between 0 and 90 exclusive."
    try:
        angle_rad = math.radians(angle_deg)
        height = distance * math.tan(angle_rad)
        return height, None
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

# Add more geometry solvers as needed: