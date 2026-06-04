# Instructions
mcp_instruction = """
Provide tools for scientific calculations related to Material Science.
"""
permeability_calculation_instruction = """
Calculate permeability using the seepage distance method.
K = L² · μ · φ / (2 · t · ΔP)
"""
infiltration_time_calculation_instruction = """
Calculate permeability using the seepage distance method.
t = μ · φ · L² / (2 · K · ΔP)
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
"""
infiltration_front_position_multiple_time_instruction = """
Calculate infiltration front position at multiple times (for graph making).
z(t) = sqrt(2 · K · ΔP · t / (μ · φ))
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
