import pytest
# Project dependencies
from permeability.permeability import SeepageDistance
from permeability.utils.UnitConverter import (
    darcy2m2,
    m22darcy
)


t = 1e2
L = 0.003
mu = 0.192
phi = 0.445
dP = 1e4
K = 3.8448e-13


def test_permeability_permeability():
    result = SeepageDistance.calculate_permeability(
        t=t,
        L=L,
        mu=mu,
        phi=phi,
        dP=dP
    )
    assert result == pytest.approx(4e-13)


def test_permeability_time():
    result = SeepageDistance.calculate_infiltration_time(
        K=K,
        L=L,
        mu=mu,
        phi=phi,
        dP=dP
    )
    assert result == pytest.approx(1e2)


def test_darcy_m2():
    m2 = 3.8448e-13
    darcy = m22darcy(m2)
    assert darcy == pytest.approx(0.3895743469)
    assert darcy2m2(darcy) == pytest.approx(m2)
