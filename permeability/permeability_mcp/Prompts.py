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
m2darcy_instruction = """
Convert m^2 to Darcy or convert darcy to m^2
If you fill the m^2 field, you will get the result converted to Darcy.
If you fill the Darcy field, you will get the result converted to m^2.
If you fill two fields, values in two fields will both get converted.
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
anisotropic_darcy_flux_instruction = """
You must type in one of the permeability tensor.
Compute Darcy flux and related quantities for anisotropic media.
Contains 'darcy_velocity' (m/s), 'flux_magnitude' (m/s),
'velocity_angle' (deg from pressure gradient direction),
and optionally 'area_flux' (m³/s per m² of given area).
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
Kx_meaning = "Permeability in x-direction (warp/fiber direction) (m²)"
Ky_meaning = "Permeability in y-direction (weft direction) (m²)"
Kz_meaning = "Permeability in z-direction (through-thickness) (m²)"
isotopic_K_meaning = "Isotropic permeability (m²)"
K_in_plane_meaning = "In-plane permeability (x and y directions) (m²)"
K_out_plane_meaning = "Out-of-plane permeability (z direction) (m²)"
from_principal_value_meaning = """
Construct a permeability tensor from principal direction permeabilities as the anisotropic permeability tensor.

This is the standard constructor for orthotropic materials
where principal axes align with the coordinate system.
"""
from_isotopic_meaning = """
Construct an isotropic permeability tensor as the anisotropic permeability tensor.

Kx = Ky = Kz = K
"""
from_transversely_isotopic_meaning = """
Construct a transversely isotropic permeability tensor as the anisotropic permeability tensor.

Kx = Ky = K_in_plane
Kz = K_out_plane

This model is appropriate for unidirectional fiber bundles.
"""
grad_p_meaning = "Pressure gradient vector (Pa/m)"
area_normal_meaning = """
Unit normal vector of the cross-section area.
If provided, computes the flux through that specific plane.
"""
