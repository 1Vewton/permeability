# Instructions
mcp_instruction = """
Provide tools for scientific calculations related to Material Science.
"""
permeability_calculation_instruction = """
Calculate permeability using the seepage distance method.
K = L² · μ · φ / (2 · t · ΔP)
If you fill the p_c field that is optional to fill, you will get the result corrected by the capillary pressure:
K = μ · φ · L² / (2 · t · (ΔP + p_c))
"""
infiltration_time_calculation_instruction = """
Calculate total time for fluid to fully penetrate the sample.
t = μ · φ · L² / (2 · K · ΔP)
If you fill the p_c field that is optional to fill, you will get the result corrected by the capillary pressure:
t = μ · φ · L² / (2 · K · (ΔP + p_c))
"""
m22darcy_instruction = """
Convert m^2 to Darcy
"""
darcy2m2_instruction = """
Convert Darcy to m^2
"""
infiltration_front_position_instruction = """
Calculate infiltration front position at given time(s).
z(t) = sqrt(2 · K · ΔP · t / (μ · φ))
If you fill the p_c field that is optional to fill, you will get the result corrected by the capillary pressure:
z(t) = sqrt(2 · K · (ΔP + p_c) · t / (μ · φ))
"""
infiltration_front_position_multiple_time_instruction = """
Calculate infiltration front position at multiple times (for graph making).
z(t) = sqrt(2 · K · ΔP · t / (μ · φ))
If you fill the p_c field that is optional to fill, you will get the result corrected by the capillary pressure:
z(t) = sqrt(2 · K · (ΔP + p_c) · t / (μ · φ))
"""
capillary_pressure_calculation_instruction = """
Calculate capillary pressure using the Young-Laplace equation.
pc = 2 · γ · cos(θ) / r
"""
pressure_difference_calculation_instruction = """
Calculate pressure difference using the seepage distance method.
ΔP = μ · φ · L² / (2 · K · t)
If you fill the p_c field that is optional to fill, you will get the result corrected by the capillary pressure:
ΔP = μ · φ · L² / (2 · K · t) - p_c
"""
# Seepage Distance Calculation
L_meaning = "Sample length/thickness along flow direction (m)"
mu_meaning = "Dynamic viscosity of the fluid (Pa·s)"
phi_meaning = "Porosity of the porous medium (dimensionless, 0 < phi <= 1)"
t_meaning = "Total time for fluid to fully penetrate the sample (s)"
multi_t_meaning = "Total time recorded for multiple rounds for fluid to fully penetrate the sample (s)"
dP_meaning = "Constant pressure difference across the sample (Pa)"
K_meaning = "Permeability (m²)"
m2K_meaning = "Permeability in m^2"
darcyK_meaning = "Permeability in Darcy"
z_meaning = "Infiltration front position at given time(s)"
p_c_meaning = "Capillary pressure (Pa)"
theta_meaning = "Contact angle (wetting angle) (Degrees)"
gamma_meaning = "Surface tension of the liquid (N/m)"
r_meaning = "Equivalent pore radius (m)"
