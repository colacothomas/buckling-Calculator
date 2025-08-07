
import streamlit as st
import math

st.title("Piston Rod Buckling Calculator (Excel-Verified)")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
ps = st.sidebar.number_input("System Pressure (pS) [bar]", value=200.0)
dk = st.sidebar.number_input("Piston Diameter (Dk) [mm]", value=90.0)
ds = st.sidebar.number_input("Rod Diameter (Ds) [mm]", value=50.0)
dho = st.sidebar.number_input("Inside Hollow Rod Diameter (Dho) [mm]", value=0.0)
da = st.sidebar.number_input("Outside Barrel Diameter (Da) [mm]", value=95.0)
ss = st.sidebar.number_input("Proof Stress (sS) [N/mm²]", value=350.0)
safety_factor = st.sidebar.number_input("Safety Factor (S)", value=2.5)
h = st.sidebar.number_input("Stroke (H) [mm]", value=950.0)
l = st.sidebar.number_input("Mounting Distance (L) [mm]", value=1100.0)

mounting_options = {
    "bearing - bearing (1.0)": 1.0,
    "fixed - bearing (0.7)": 0.7,
    "fixed - free (2.0)": 2.0,
    "fixed - fixed (4.0)": 4.0
}
mounting_label = st.sidebar.selectbox("Mounting Type", options=list(mounting_options.keys()))
k_factor = mounting_options[mounting_label]

e = st.sidebar.number_input("Elasticity Modulus (E) [N/mm²]", value=210000.0)
a = st.sidebar.number_input("Installation Angle (a) [°]", value=23.0)

# Constants
PI = math.pi
density = 7.85e-6  # g/mm³
g = 9.81  # m/s²

# Areas
A_rod = PI * ds**2 / 4
A_piston = PI * dk**2 / 4
A_annulus = A_piston - A_rod

# Push Force (Excel logic)
Fd = ps * A_annulus / 1000  # [kN]

# Press Stress (Excel logic)
sd = ps  # [N/mm²], same as system pressure

# Resistance Moment Wb (solid rod or hollow)
Wb = (PI * ds**3) / 32 if dho == 0 else PI * (ds**4 - dho**4) / (32 * ds)

# Line Load q (dead weight)
q = density * g * A_rod  # N/mm

# Bending Stress
sb = q * l**2 / (8 * Wb)

# Buckling Stress
sk = sd + sb

# Free Buckling Length Lk (with angle correction)
Lk = l * k_factor * math.sqrt(1 + (h / l)**2 * math.sin(math.radians(a))**2)

# Moment of Inertia I (solid rod assumed)
I = (PI * ds**4) / 64

# Buckling Force Fk
Fk = (PI**2 * e * I) / (Lk**2) / 1000  # [kN]

# Safety Factor
Svorh = Fk / Fd if Fd != 0 else float('inf')

# Slenderness Ratio
radius_gyration = math.sqrt(I / A_rod)
slenderness_ratio = Lk / radius_gyration

# Euler/Johnson Boundary Line
boundary_line = 2 * PI * math.sqrt(e / (2 * ss))

# Trial Rod Diameter
trial_d = ((Fk * 1000 * (Lk**2)) / (PI**2 * e * (PI / 32)))**(1/3)

# Output
st.header("Results")
st.write(f"**Line Load q (dead weight):** {q:.4f} N/mm")
st.write(f"**Push Force Fd:** {Fd:.5f} kN")
st.write(f"**Press Stress sd:** {sd:.5f} N/mm²")
st.write(f"**Resistance Moment Wb:** {Wb:.6f} mm³")
st.write(f"**Bending Stress sb:** {sb:.6f} N/mm²")
st.write(f"**Buckling Stress sk:** {sk:.6f} N/mm²")
st.write(f"**Free Buckling Length Lk:** {Lk:.2f} mm")
st.write(f"**Buckling Force Fk:** {Fk:.5f} kN")
st.write(f"**Existing Safety Factor Svorh:** {Svorh:.6f}")
st.write(f"**Boundary Line (Euler/Johnson):** {boundary_line:.6f}")
st.write(f"**Slenderness Ratio (l/k):** {slenderness_ratio:.6f}")
st.write(f"**Ideal Trial Rod Diameter (Euler):** {trial_d:.6f} mm")

if slenderness_ratio < boundary_line:
    st.success("Slenderness ratio is within Euler limits → Euler method valid")
else:
    st.warning("Slenderness ratio exceeds boundary → Johnson method recommended")
