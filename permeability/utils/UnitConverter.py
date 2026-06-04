def m22darcy(
        m2K: float
) -> float:
    '''
    Convert m^2 to Darcy
    :param m2K: Permeability in m^2
    :return: Permeability in Darcy
    '''
    return m2K * 1.01325e+12


def darcy2m2(
        darcyK: float
) -> float:
    '''
    Convert Darcy to m^2
    :param darcyK: Permeability in Darcy
    :return: Permeability in m^2
    '''
    return darcyK * 0.986923e-12
