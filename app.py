import streamlit as st
import math

# Title
st.title("Piston Rod Buckling Calculator")

# Input Fields
mounting_options = {
    "bearing - bearing": 1.0,
    "fixed - bearing": 0.7,
    "fixed - free": 2.0,
    "fixed - fixed": 4.0
}

mounting_label = st.selectbox("Select Mounting Type", list(mounting_options.keys()))
k_factor = mounting_options[mounting_label]

Ds = st.number_input("Rod Diameter Ds (mm)", value=50.0)
Dk = st.number_input("Piston Diameter Dk (mm)", value=90.0)
Dho = st.number_input("Hollow Rod Inner Diameter Dho (mm)", value=0.0)
L = st.number_input("Mounting Distance L (mm)", value=1100.0)
H = st.number_input("Stroke H (mm)", value=950.0)
a = st.number_input("Angle α (degrees)", value=23.0)
ps_nmm2 = st.number_input("Operating Pressure (N/mm²)", value=200.0)
safety_factor = st.number_input("Safety Factor", value=2.5)

# Constants
PI = math.pi
e = 210000  # Modulus of elasticity (N/mm²)
rho = 6.78e-5  # Density (g/mm³)

# Calculated Geometry
A_piston = (PI / 4) * (Dk**2 - Ds**2)
I = PI * (Ds**4 - Dho**4) / 64  # Moment of inertia
Wb = (PI * (Ds**4 - Dho**4)) / (32 * Ds)  # Resistance moment

# Line load q (N/mm)
q = rho * A_piston * 1000  # N/mm

# Push force (kN)
Fd = ps_nmm2 * A_piston / 1000  # kN

# Press stress sd (N/mm²)
sd = (Fd * 1000) / (PI * (Ds**2 - Dho**2) / 4) + \
     q * (L + H) / 2 / (PI * (Ds**2 - Dho**2) / 4) * math.sin(math.radians(a))

# Bending stress sb (N/mm²)
sb = (q * (L + H)**2 / (8 * Wb)) * math.cos(math.radians(a))

# Free buckling length
Lk = k_factor * (L + H)

# Buckling stress sk (N/mm²)
sk = (PI**2 * e * I) / (Lk**2) / ((PI * (Ds**2 - Dho**2)) / 4)

# Buckling force Fk (kN)
Fk = sk * (PI / 4) * (Ds**2 - Dho**2) / 1000  # kN

# Existing safety factor
Svorh = Fk / (Fd + (q * (L + H) / 2 * math.sin(math.radians(a)) / 1000))

# Ideal Piston Rod Diameter using Euler
Eu = ((64 * Fd * safety_factor * 1000 * Lk**2) / (L * PI**3 * e))**0.25
slenderness_ratio = Lk * 4 / Eu

# Output
st.header("Results")

st.markdown(f"**Line Load q:** {q:.2f} N/mm")
st.markdown(f"**Push Force Fd:** {Fd:.2f} kN")
st.markdown(f"**Press Stress sd:** {sd:.2f} N/mm²")
st.markdown(f"**Resistance Moment Wb:** {Wb:.2f} mm³")

st.markdown(
    f"**Bending Stress sb:** {sb:.2f} N/mm²  \n"
    "Formula: `sb = q × (L + H)² ÷ (8 × Wb) × cos(π / 180 × α)`"
)

st.markdown(f"**Buckling Stress sk:** {sk:.2f} N/mm²")
st.markdown(f"**Free Buckling Length Lk:** {Lk:.2f} mm")
st.markdown(f"**Buckling Force Fk:** {Fk:.2f} kN")
st.markdown(f"**Existing Safety Factor Svorh:** {Svorh:.2f}")
st.markdown(f"**Ideal Rod Diameter (Euler Trial) Eu:** {Eu:.2f} mm")
st.markdown(f"**Slenderness Ratio:** {slenderness_ratio:.2f}")
