import numpy as np


def calculate_permeability(
        L: float,
        mu: float,
        phi: float,
        t: float,
        dP: float,
) -> float:
    '''
    Calculate permeability using the seepage distance method.
    K = L² · μ · φ / (2 · t · ΔP)
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
    return (L * L * mu * phi) / (2 * t * dP)


def calculate_infiltration_time(
        L: float,
        mu: float,
        phi: float,
        K: float,
        dP: float
) -> float:
    '''
    Calculate permeability using the seepage distance method.
    t = μ · φ · L² / (2 · K · ΔP)
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
    return (mu * phi * L * L) / (2 * K * dP)


def calculate_infiltration_front_position(
        K: float,
        mu: float,
        phi: float,
        dP: float,
        t: float,
) -> float:
    '''
    Calculate infiltration front position at given time(s).
    z(t) = sqrt(2 · K · ΔP · t / (μ · φ))
    :param K: Permeability (m^2)
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
    return np.sqrt((2 * K * dP * t) / (mu * phi))


def calculate_infiltration_front_position_with_multiple_time(
        K: float,
        mu: float,
        phi: float,
        dP: float,
        t: np.ndarray,
) -> np.ndarray:
    '''
    Calculate infiltration front position at multiple times (for graph making).
    z(t) = sqrt(2 · K · ΔP · t / (μ · φ))
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
    return np.sqrt((2 * K * dP * t) / (mu * phi))
