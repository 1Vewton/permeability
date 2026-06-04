import pytest
import numpy as np
# Project dependencies
from permeability.permeability import Seepage
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
    result = Seepage.calculate_permeability(
        t=t,
        L=L,
        mu=mu,
        phi=phi,
        dP=dP
    )
    assert result == pytest.approx(4e-13)


def test_permeability_time():
    result = Seepage.calculate_infiltration_time(
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


def test_infiltration_front_position():
    result1 = 0
    test_result_1 = Seepage.calculate_infiltration_front_position(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=0
    )
    assert test_result_1 == pytest.approx(result1)
    result2 = 0.005
    test_result_2 = Seepage.calculate_infiltration_front_position(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=120
    )
    assert test_result_2 == pytest.approx(result2)
    result3 = 0.0025
    test_result_3 = Seepage.calculate_infiltration_front_position(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=30
    )
    assert test_result_3 == pytest.approx(result3)


def test_infiltration_front_position_with_multiple_time():
    result = np.array([0.0, 0.0025, 0.005])
    test_result = Seepage.calculate_infiltration_front_position_with_multiple_time(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=np.array([0, 30, 120])
    )
    np.testing.assert_array_equal(result, test_result)
