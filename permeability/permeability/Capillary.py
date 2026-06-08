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


def calculate_infiltration_front_position_with_capillary_correction(
        K: float,
        mu: float,
        phi: float,
        dP: float,
        t: float,
        p_c: float
) -> float:
    '''
    Calculate infiltration front position with capillary force correction at given time(s).
    z(t) = sqrt(2 · K · (ΔP + p_c) · t / (μ · φ))
    :param K: Permeability (m^2)
    :param p_c: capillary pressure (Pa)
    :param mu: Dynamic viscosity of the fluid (Pa·s)
    :param phi: Porosity of the porous medium (dimensionless, 0 < phi <= 1)
    :param dP: Constant pressure difference across the sample (Pa)
    :param t: Total time recorded for fluid to fully penetrate the sample (s)
    :return: z, the infiltration front position at given time
    '''
    if mu <= 0 or phi <= 0:
        raise ValueError("mu and phi cannot be smaller than 0")
    if phi > 1 or phi < 0:
        raise ValueError("phi must be between 0 and 1")
    if K <= 0:
        raise ValueError("K must be greater than 0")
    if t < 0:
        raise ValueError("t must be greater than 0")
    if dP <= 0:
        raise ValueError("dP must be greater than 0")
    return np.sqrt((2 * K * (dP+p_c) * t) / (mu * phi))


def calculate_infiltration_front_position_with_multiple_time_with_capillary_correction(
        K: float,
        mu: float,
        phi: float,
        dP: float,
        t: np.ndarray,
        p_c: float
) -> np.ndarray:
    '''
    Calculate infiltration front position with capillary force correction at multiple times (for graph making).
    z(t) = sqrt(2 · K · (ΔP + p_c) · t / (μ · φ))
    :param p_c: capillary pressure (Pa)
    :param K: Permeability (m^2)
    :param mu: Dynamic viscosity of the fluid (Pa·s)
    :param phi: Porosity of the porous medium (dimensionless, 0 < phi <= 1)
    :param dP: Constant pressure difference across the sample (Pa)
    :param t: Total time recorded for multiple rounds for fluid to fully penetrate the sample (s)
    :return: z, the infiltration front position at given time
    '''
    if mu <= 0 or phi <= 0:
        raise ValueError("mu and phi cannot be smaller than 0")
    if phi > 1 or phi < 0:
        raise ValueError("phi must be between 0 and 1")
    if K <= 0:
        raise ValueError("K must be greater than 0")
    if not np.all(t >= 0):
        raise ValueError("t must be greater than 0")
    if dP <= 0:
        raise ValueError("dP must be greater than 0")
    return np.sqrt((2 * K * (dP+p_c) * t) / (mu * phi))


def calculate_pressure_difference_with_capillary_correction(
        L: float,
        mu: float,
        phi: float,
        K: float,
        t: float,
        p_c: float
) -> float:
    '''
    Calculate pressure difference using the seepage distance method with capillary correction.
    ΔP = μ · φ · L² / (2 · K · t) - p_c
    :param L: Sample length/thickness along flow direction (m)
    :param mu: Dynamic viscosity of the fluid (Pa·s)
    :param phi: Porosity of the porous medium (dimensionless, 0 < phi <= 1)
    :param K: Permeability (m^2)
    :param t, Total time for fluid to fully penetrate the sample (s)
    :return: dP, Constant pressure difference across the sample (Pa)
    '''
    if K <= 0 or t <= 0:
        raise ValueError("dP and K cannot be smaller than 0")
    if mu <= 0:
        raise ValueError("mu cannot be <= 0")
    if phi > 1 or phi < 0:
        raise ValueError("phi must be between 0 and 1")
    if L <= 0:
        raise ValueError("L must be greater than 0")
    return (mu * phi * L * L) / (2 * K * t) - p_c
