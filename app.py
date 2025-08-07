
import streamlit as st
import math

st.title("Piston Rod Buckling Calculator (Excel-Verified)""")

# Sidebar Inputs
st.sidebar.header("Input Parameters""")
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
g = 9.81  # m/s²

PI = math.pi
density = 7.85e-6  # g/mm³
g = 9.81  # m/s²

# Convert pressure from bar to N/mm²
ps_nmm2 = ps * 0.1

# Areas
A_rod = PI * ds**2 / 4
A_piston = PI * dk**2 / 4

# ✅ Corrected Push Force (Fd) with units
Fd = ps_nmm2 * A_piston / 1000  # kN

# ✅ Press Stress (input value)
sd = ps_nmm2  # N/mm²

# ✅ Resistance Moment
if dho == 0:
    Wb = (PI * ds**3) / 32
else:
    Wb = PI * (ds**4 - dho**4) / (32 * ds)

# ✅ Line Load q
q = density * g * A_rod  # N/mm

# ✅ Bending Stress
sb = q * l**2 / (8 * Wb)

# ✅ Buckling Stress
sk = sd + sb

# ✅ Free Buckling Length with angle
Lk = l * k_factor * math.sqrt(1 + (h / l)**2 * math.sin(math.radians(a))**2)

# ✅ Moment of Inertia
I = (PI * ds**4) / 64

# ✅ Buckling Force
Fk = (PI**2 * e * I) / (Lk**2) / 1000  # kN

# ✅ Safety Factor
Svorh = Fk / Fd if Fd else float("inf""")

# ✅ Radius of gyration
k_radius = math.sqrt(I / A_rod)

# ✅ Slenderness ratio
slenderness_ratio = Lk / k_radius

# ✅ Euler/Johnson boundary
boundary_line = 2 * PI * math.sqrt(e / (2 * ss))

# ✅ Ideal piston rod diameter
trial_d = ((Fk * 1000 * (Lk**2)) / (PI**2 * e * (PI / 32)))**(1/3)

# Output section
st.header("Results""")
st.write(f"**Line Load q (dead weight):** {q:.2f} N/mm""")
st.markdown(f"""**Push Force Fd:** {Fd:.2f} kN  
Formula: `Fd = pS × π/4 × Dk² ÷ 1000`""")
st.markdown(f"""**Press Stress sd:** {sd:.2f} N/mm²  
Formula: `sd = pS × 0.1`""")
st.markdown(f"""**Resistance Moment Wb:** {Wb:.2f} mm³  
Formula: `Wb = π × Ds³ ÷ 32` (solid rod)""")
st.markdown(f"""**Bending Stress sb:** {sb:.2f} N/mm²  
Formula: `sb = q × L² ÷ (8 × Wb)`""")
st.markdown(f"""**Buckling Stress sk:** {sk:.2f} N/mm²  
Formula: `sk = sd + sb`""")
st.markdown(f"""**Free Buckling Length Lk:** {Lk:.2f} mm  
Formula: `Lk = L × k × √[1 + (H/L)² × sin²(a)]`""")
st.markdown(f"""**Buckling Force Fk:** {Fk:.2f} kN  
Formula: `Fk = π² × E × I ÷ Lk² ÷ 1000`""")
st.markdown(f"""**Existing Safety Factor Svorh:** {Svorh:.2f}  
Formula: `S = Fk ÷ Fd`""")
st.markdown(f"""**Boundary Line (Euler/Johnson):** {boundary_line:.2f}  
Formula: `2π × √(E ÷ 2sS)`""")
st.markdown(f"""**Slenderness Ratio (l/k):** {slenderness_ratio:.2f}  
Formula: `Lk ÷ k_radius`""")
st.markdown(f"""**Ideal Trial Rod Diameter (Euler):** {trial_d:.2f} mm  
Formula: Cubic root of `Fk × Lk² / (π² × E × π/32)`""")

if slenderness_ratio < boundary_line:
    st.success("Slenderness ratio is within Euler limits → Euler method valid""")
else:
    st.warning("Slenderness ratio exceeds boundary → Use Johnson method""")
