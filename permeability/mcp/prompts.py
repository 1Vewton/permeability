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
# Seepage Distance Calculation
L_meaning = "Sample length/thickness along flow direction (m)"
mu_meaning = "Dynamic viscosity of the fluid (Pa·s)"
phi_meaning = "Porosity of the porous medium (dimensionless, 0 < phi <= 1)"
t_meaning = "Total time for fluid to fully penetrate the sample (s)"
dP_meaning = "Constant pressure difference across the sample (Pa)"
K_meaning = "Permeability (m²)"
