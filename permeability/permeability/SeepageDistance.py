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
    if dP == 0 or t == 0:
        raise ValueError("dP and t cannot be 0")
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
    if K == 0 or dP == 0:
        raise ValueError("dP and K cannot be 0")
    return (mu * phi * L * L) / (2 * K * dP)
