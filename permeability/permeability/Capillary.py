import numpy as np


def calculate_capillary_pressure(
        gamma: float,
        theta: float,
        r: float
) -> float:
    '''
    Calculate capillary pressure using the Young-Laplace equation.
    p_c = 2 · γ · cos(θ) / r
    :param gamma: Surface tension of the liquid (N/m)
    :param theta: Contact angle (wetting angle) (Degrees)
    :param r: Equivalent pore radius (m)
    :return: p_c, capillary pressure (Pa)
    '''
    if gamma <= 0:
        raise ValueError('gamma must be greater than 0')
    if r <= 0:
        raise ValueError('r must be greater than 0')
    rad_theta = np.deg2rad(theta)
    return (2*gamma*np.cos(rad_theta))/r


def calculate_permeability_with_capillary_correction(
        p_c: float,
        L: float,
        mu: float,
        phi: float,
        t: float,
        dP: float,
):
    '''
    Calculate permeability with capillary force correction.
    K = μ · φ · L² / (2 · t · (ΔP + p_c))
    :param p_c: capillary pressure (Pa)
    :param L: Sample length/thickness along flow direction (m)
    :param mu: Dynamic viscosity of the fluid (Pa·s)
    :param phi: Porosity of the porous medium (dimensionless, 0 < phi <= 1)
    :param t: Total time for fluid to fully penetrate the sample (s)
    :param dP: Constant pressure difference across the sample (Pa)
    :return: K, Permeability (m^2)
    '''
    if dP <= 0 or t <= 0:
        raise ValueError("dP and t cannot be smaller than 0")
    if mu <= 0:
        raise ValueError("mu cannot be <= 0")
    if phi > 1 or phi < 0:
        raise ValueError("phi must be between 0 and 1")
    if L <= 0:
        raise ValueError("L must be greater than 0")
    if p_c == -dP:
        raise ValueError("p_c + dP cannot be equal to 0")
    return (L * L * mu * phi) / (2 * t * (dP + p_c))


def calculate_infiltration_time_with_capillary_correction(
        p_c: float,
        L: float,
        mu: float,
        phi: float,
        K: float,
        dP: float
) -> float:
    '''
    Calculate permeability with capillary force correction.
    t = μ · φ · L² / (2 · K · (ΔP + p_c))
    :param p_c: capillary pressure (Pa)
    :param L: Sample length/thickness along flow direction (m)
    :param mu: Dynamic viscosity of the fluid (Pa·s)
    :param phi: Porosity of the porous medium (dimensionless, 0 < phi <= 1)
    :param K: Permeability (m^2)
    :param dP: Constant pressure difference across the sample (Pa)
    :return: t, Total time for fluid to fully penetrate the sample (s)
    '''
    if K <= 0 or dP <= 0:
        raise ValueError("dP and K cannot be smaller than 0")
    if mu <= 0:
        raise ValueError("mu cannot be <= 0")
    if phi > 1 or phi < 0:
        raise ValueError("phi must be between 0 and 1")
    if L <= 0:
        raise ValueError("L must be greater than 0")
    if p_c == -dP:
        raise ValueError("p_c + dP != 0")
    return (mu * phi * L * L) / (2 * K * (dP+p_c))
