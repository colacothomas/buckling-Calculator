
# Sample imports and constants
import math
import streamlit as st

# Constants
PI = math.pi
e = 210000  # Example: modulus of elasticity [N/mm²]
safety_factor = 2.5

# Example input values (replace with actual streamlit input collection)
ps_nmm2 = 200  # Pressure in N/mm²
Ds = 50        # Rod diameter in mm
Dk = 90        # Piston diameter in mm
Dho = 0        # Hollow rod (0 if solid)
l = 1100       # Mounting distance
H = 950        # Stroke
Lk = 2200      # Buckling length

# Cross-sectional area
A_piston = (PI / 4) * (Dk**2 - Ds**2)

# Push force
Fd = ps_nmm2 * A_piston / 1000  # kN

# Eu calculation after Fd is defined
Eu = ((64 * Fd * safety_factor * 1000 * Lk**2) / (l * PI**3 * e))**0.25
slenderness_ratio = Lk * 4 / Eu

# Streamlit output
st.write(f"Ideal Piston Rod Diameter (Eu): {Eu:.2f} mm")
st.write(f"Slenderness Ratio: {slenderness_ratio:.2f}")
