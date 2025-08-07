import streamlit as st
import math

st.title("Piston Rod Buckling Calculator")

# Input fields with default values
st.sidebar.header("Input Parameters")
ps = st.sidebar.number_input("System Pressure (pS) [bar]", value=190.0)
dk = st.sidebar.number_input("Piston Diameter (Dk) [mm]", value=60.0)
ds = st.sidebar.number_input("Rod Diameter (Ds) [mm]", value=45.0)
dho = st.sidebar.number_input("Inside Hollow Rod Diameter (Dho) [mm]", value=0.0)
da = st.sidebar.number_input("Outside Barrel Diameter (Da) [mm]", value=95.0)
ss = st.sidebar.number_input("Proof Stress (sS) [N/mm²]", value=350.0)
safety_factor = st.sidebar.number_input("Safety Factor (S)", value=2.5)
h = st.sidebar.number_input("Stroke (H) [mm]", value=950.0)
l = st.sidebar.number_input("Mounting Distance (L) [mm]", value=1200.0)

mounting_options = {
    "bearing - bearing (1.0)": 1.0,
    "fixed - bearing (0.7)": 0.7,
    "fixed - free (2.0)": 2.0,
    "fixed - fixed (4.0)": 4.0
}
mounting_label = st.sidebar.selectbox("Mounting Type", options=list(mounting_options.keys()))
k = mounting_options[mounting_label]

e = st.sidebar.number_input("Elasticity Modulus (E) [N/mm²]", value=210000.0)
a = st.sidebar.number_input("Installation Angle (a) [°]", value=45.0)

# Area of piston
area = math.pi * (dk**2 - ds**2) / 4  # mm²
fd = ps * 1e5 * area / 1e3  # Convert bar to Pa (N/mm²), then to kN
sd = (fd * 1e3) / area  # N/mm²

# Resistance moment Wb
if dho == 0:
    wb = (math.pi * ds**3) / 32  # mm³
else:
    wb = (math.pi * (ds**4 - dho**4)) / (32 * ds)  # mm³

# Line load q (due to dead weight)
density_steel = 7.85e-6  # kg/mm³
q = -density_steel * math.pi * ds**2 / 4 * 9.81  # N/mm

# Bending stress sb
sb = abs(q) * l**2 / (8 * wb)

# Total stress sk
sk = sd + sb

# Free buckling length Lk
lk = l * k * math.sqrt(1 + (h / l)**2 * math.sin(math.radians(a))**2)

# Buckling force Fk (solid rod)
i = (ds**4 - dho**4) * math.pi / 64 if dho > 0 else math.pi * ds**4 / 64
fk = (math.pi**2 * e * i) / (lk**2) / 1e3  # kN

# Existing safety factor Svorh
svorh = fk / fd if fd != 0 else float('inf')

# Slenderness ratio and boundary
slenderness_ratio = lk / ds
boundary = 32.8 * math.sqrt(e / ss)

# Ideal piston rod diameter from Euler
ideal_dia = ((64 * fk * 1e3 * lk**2) / (math.pi**3 * e))**0.25  # mm

# Outputs
st.header("Results")
st.write(f"**Line Load q (dead weight):** {q:.6f} N/mm")
st.write(f"**Push Force Fd:** {fd:.3f} kN")
st.write(f"**Press Stress sd:** {sd:.3f} N/mm²")
st.write(f"**Resistance Moment Wb:** {wb:.3f} mm³")
st.write(f"**Bending Stress sb:** {sb:.3f} N/mm²")
st.write(f"**Buckling Stress sk:** {sk:.3f} N/mm²")
st.write(f"**Free Buckling Length Lk:** {lk:.2f} mm")
st.write(f"**Buckling Force Fk:** {fk:.3f} kN")
st.write(f"**Existing Safety Factor Svorh:** {svorh:.3f}")
st.write(f"**Boundary Line (Euler/Johnson):** {boundary:.3f}")
st.write(f"**Trial Rod Dia (Euler):** {ideal_dia:.3f} mm")
st.write(f"**Slenderness Ratio (l/k):** {slenderness_ratio:.3f}")

if slenderness_ratio < boundary:
    st.success("Slenderness ratio is less than boundary → Euler valid")
else:
    st.warning("Slenderness ratio exceeds boundary → Euler not valid")

st.write(f"**Ideal Piston Rod Diameter:** {ideal_dia:.3f} mm")
