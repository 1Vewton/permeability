import pytest
import numpy as np

# Project dependencies
from permeability.permeability.Seepage import (
    calculate_permeability,
    calculate_infiltration_time,
    calculate_infiltration_front_position,
    calculate_infiltration_front_position_with_multiple_time,
    calculate_pressure_difference,
)
from permeability.permeability.Capillary import (
    calculate_capillary_pressure,
    calculate_permeability_with_capillary_correction,
    calculate_infiltration_time_with_capillary_correction,
    calculate_infiltration_front_position_with_capillary_correction,
    calculate_infiltration_front_position_with_multiple_time_with_capillary_correction,
    calculate_pressure_difference_with_capillary_correction,
)
from permeability.permeability.AnisotropicTensor import (
    PermeabilityTensor,
    FullTensor,
    anisotropic_darcy_flux,
    anisotropy_evolution,
)
from permeability.utils.UnitConverter import (
    darcy2m2,
    m22darcy,
)


# =============================================================================
# Seepage distance method - basic calculations
# =============================================================================

t = 1e2
L = 0.003
mu = 0.192
phi = 0.445
dP = 1e4
K = 3.8448e-13


def test_permeability_permeability():
    result = calculate_permeability(
        t=t,
        L=L,
        mu=mu,
        phi=phi,
        dP=dP,
    )
    assert result == pytest.approx(4e-13)


def test_permeability_time():
    result = calculate_infiltration_time(
        K=K,
        L=L,
        mu=mu,
        phi=phi,
        dP=dP,
    )
    assert result == pytest.approx(1e2)


def test_permeability_dP():
    result = calculate_pressure_difference(
        K=K,
        L=L,
        mu=mu,
        phi=phi,
        t=t,
    )
    assert result == pytest.approx(dP)


def test_darcy_m2():
    m2 = 3.8448e-13
    darcy = m22darcy(m2)
    assert darcy == pytest.approx(0.3895743469)
    assert darcy2m2(darcy) == pytest.approx(m2)


def test_infiltration_front_position():
    result1 = 0
    test_result_1 = calculate_infiltration_front_position(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=0,
    )
    assert test_result_1 == pytest.approx(result1)

    result2 = 0.005
    test_result_2 = calculate_infiltration_front_position(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=120,
    )
    assert test_result_2 == pytest.approx(result2)

    result3 = 0.0025
    test_result_3 = calculate_infiltration_front_position(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=30,
    )
    assert test_result_3 == pytest.approx(result3)


def test_infiltration_front_position_with_multiple_time():
    result = np.array([0.0, 0.0025, 0.005])
    test_result = calculate_infiltration_front_position_with_multiple_time(
        K=1.284e-13,
        mu=0.192,
        phi=0.642,
        dP=1e5,
        t=np.array([0, 30, 120]),
    )
    np.testing.assert_array_equal(result, test_result)


def test_calculate_permeability_negative_phi():
    with pytest.raises(ValueError):
        calculate_permeability(L=1, mu=1, phi=-0.1, t=1, dP=1)


# =============================================================================
# Capillary pressure correction
# =============================================================================


def test_calculate_capillary_pressure():
    p_c = calculate_capillary_pressure(gamma=0.072, theta=30, r=1e-6)
    expected = 2 * 0.072 * np.cos(np.deg2rad(30)) / 1e-6
    assert p_c == pytest.approx(expected)


def test_calculate_capillary_pressure_zero_contact_angle():
    # Perfectly wetting: cos(0) = 1
    p_c = calculate_capillary_pressure(gamma=0.072, theta=0, r=1e-6)
    expected = 2 * 0.072 * 1 / 1e-6
    assert p_c == pytest.approx(expected)


def test_calculate_capillary_pressure_non_wetting():
    # Non-wetting: cos(180) = -1 → negative capillary pressure
    p_c = calculate_capillary_pressure(gamma=0.072, theta=180, r=1e-6)
    expected = 2 * 0.072 * (-1) / 1e-6
    assert p_c == pytest.approx(expected)


def test_calculate_capillary_pressure_zero_gamma():
    with pytest.raises(ValueError):
        calculate_capillary_pressure(gamma=0, theta=30, r=1e-6)


def test_calculate_capillary_pressure_zero_radius():
    with pytest.raises(ValueError):
        calculate_capillary_pressure(gamma=0.072, theta=30, r=0)


# --- capillary-corrected permeability ---


def test_permeability_with_capillary_correction():
    p_c = calculate_capillary_pressure(gamma=0.072, theta=30, r=1e-6)
    # Without correction
    K_no_corr = calculate_permeability(L=0.003, mu=0.192, phi=0.445, t=100, dP=1e4)
    # With correction: effective driving force is larger → larger K
    K_corr = calculate_permeability_with_capillary_correction(
        L=0.003, mu=0.192, phi=0.445, t=100, dP=1e4, p_c=p_c
    )
    # dP + p_c > dP → K_corr < K_no_corr (inverse relationship)
    assert K_corr < K_no_corr
    # Verify exact value
    expected = (0.003**2 * 0.192 * 0.445) / (2 * 100 * (1e4 + p_c))
    assert K_corr == pytest.approx(expected)


def test_permeability_with_capillary_correction_invalid():
    with pytest.raises(ValueError):
        calculate_permeability_with_capillary_correction(
            L=1, mu=1, phi=0.5, t=1, dP=1, p_c=-1  # p_c + dP = 0
        )


# --- capillary-corrected infiltration time ---


def test_infiltration_time_with_capillary_correction():
    p_c = 124.71
    t_no_corr = calculate_infiltration_time(L=0.003, mu=0.192, phi=0.445, K=3.8448e-13, dP=1e4)
    t_corr = calculate_infiltration_time_with_capillary_correction(
        L=0.003, mu=0.192, phi=0.445, K=3.8448e-13, dP=1e4, p_c=p_c
    )
    # Larger effective dP → shorter time
    assert t_corr < t_no_corr
    expected = (0.192 * 0.445 * 0.003**2) / (2 * 3.8448e-13 * (1e4 + p_c))
    assert t_corr == pytest.approx(expected)


# --- capillary-corrected front position ---


def test_infiltration_front_position_with_capillary_correction():
    p_c = 124.71
    z_no_corr = calculate_infiltration_front_position(
        K=1.284e-13, mu=0.192, phi=0.642, dP=1e5, t=120,
    )
    z_corr = calculate_infiltration_front_position_with_capillary_correction(
        K=1.284e-13, mu=0.192, phi=0.642, dP=1e5, t=120, p_c=p_c,
    )
    # Larger effective dP → faster front movement
    assert z_corr > z_no_corr
    expected = np.sqrt((2 * 1.284e-13 * (1e5 + p_c) * 120) / (0.192 * 0.642))
    assert z_corr == pytest.approx(expected)


# --- capillary-corrected front position (multiple times) ---


def test_infiltration_front_position_multiple_time_with_capillary_correction():
    p_c = 124.71
    z_no_corr = calculate_infiltration_front_position_with_multiple_time(
        K=1.284e-13, mu=0.192, phi=0.642, dP=1e5,
        t=np.array([0, 30, 120]),
    )
    z_corr = calculate_infiltration_front_position_with_multiple_time_with_capillary_correction(
        K=1.284e-13, mu=0.192, phi=0.642, dP=1e5,
        t=np.array([0, 30, 120]), p_c=p_c,
    )
    assert np.all(z_corr >= z_no_corr)
    expected = np.sqrt((2 * 1.284e-13 * (1e5 + p_c) * np.array([0, 30, 120])) / (0.192 * 0.642))
    np.testing.assert_array_equal(z_corr, expected)


# --- capillary-corrected pressure difference ---


def test_pressure_difference_with_capillary_correction():
    p_c = 124.71
    dP_no_corr = calculate_pressure_difference(L=0.003, mu=0.192, phi=0.445, K=3.8448e-13, t=100)
    dP_corr = calculate_pressure_difference_with_capillary_correction(
        L=0.003, mu=0.192, phi=0.445, K=3.8448e-13, t=100, p_c=p_c,
    )
    # dP_corr = dP_no_corr - p_c
    assert dP_corr == pytest.approx(dP_no_corr - p_c)


# =============================================================================
# PermeabilityTensor - Anisotropic tensor
# =============================================================================


def test_permeability_tensor_from_principal_values():
    tensor = PermeabilityTensor.from_principal_values(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    assert tensor.Kx == pytest.approx(1e-12)
    assert tensor.Ky == pytest.approx(5e-13)
    assert tensor.Kz == pytest.approx(1e-13)


def test_permeability_tensor_from_isotopic():
    tensor = PermeabilityTensor.from_isotopic(K=1e-12)
    assert tensor.Kx == tensor.Ky == tensor.Kz == pytest.approx(1e-12)


def test_permeability_tensor_from_transversely_isotropic():
    tensor = PermeabilityTensor.from_transversely_isotropic(
        K_in_plane=1e-12, K_out_plane=1e-13
    )
    assert tensor.Kx == tensor.Ky == pytest.approx(1e-12)
    assert tensor.Kz == pytest.approx(1e-13)


def test_permeability_tensor_invalid_values():
    with pytest.raises(ValueError):
        PermeabilityTensor(Kx=-1, Ky=1e-12, Kz=1e-12)
    with pytest.raises(ValueError):
        PermeabilityTensor(Kx=1e-12, Ky=0, Kz=1e-12)
    with pytest.raises(ValueError):
        PermeabilityTensor(Kx=1e-12, Ky=1e-12, Kz=-1e-13)


def test_permeability_tensor_properties():
    tensor = PermeabilityTensor(Kx=2e-12, Ky=1e-12, Kz=5e-13)
    # in_plane_average
    assert tensor.in_plane_average == pytest.approx(1.5e-12)
    # anisotropy_ratio
    assert tensor.anisotropy_ratio == pytest.approx(1.5e-12 / 5e-13)
    # degree_of_anisotropy
    assert tensor.degree_of_anisotropy == pytest.approx(1.0 - 5e-13 / 2e-12)
    # tensor (3x3 diagonal)
    expected = np.diag([2e-12, 1e-12, 5e-13])
    np.testing.assert_array_equal(tensor.tensor, expected)


def test_permeability_tensor_darcy_velocity():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    grad_p = np.array([1000, 500, 100])
    mu = 0.192
    v = tensor.darcy_velocity(grad_p, mu)
    expected_v = -(1.0 / mu) * (tensor.tensor @ grad_p)
    np.testing.assert_array_equal(v, expected_v)


def test_permeability_tensor_darcy_velocity_invalid_mu():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    with pytest.raises(ValueError):
        tensor.darcy_velocity(np.array([1000, 500, 100]), mu=0)


def test_permeability_tensor_effective_permeability():
    tensor = PermeabilityTensor(Kx=2e-12, Ky=1e-12, Kz=5e-13)
    # Direction shorthand
    assert tensor.effective_permeability_in_direction(direction='x') == pytest.approx(2e-12)
    assert tensor.effective_permeability_in_direction(direction='y') == pytest.approx(1e-12)
    assert tensor.effective_permeability_in_direction(direction='z') == pytest.approx(5e-13)
    assert tensor.effective_permeability_in_direction(direction='xy') == pytest.approx(1.5e-12)
    assert tensor.effective_permeability_in_direction(direction='avg') == pytest.approx(
        (2e-12 + 1e-12 + 5e-13) / 3.0
    )


def test_permeability_tensor_effective_permeability_arbitrary_direction():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    n = np.array([1, 0, 0])  # x-direction
    eff = tensor.effective_permeability_in_direction(direction_vector=n)
    assert eff == pytest.approx(1e-12)

    # Non-unit vector should be normalized
    n2 = np.array([2, 0, 0])
    eff2 = tensor.effective_permeability_in_direction(direction_vector=n2)
    assert eff2 == pytest.approx(1e-12)

    # 45° in xy-plane: K_eff = (Kx + Ky) / 2
    n45 = np.array([1, 1, 0]) / np.sqrt(2)
    eff45 = tensor.effective_permeability_in_direction(direction_vector=n45)
    assert eff45 == pytest.approx((1e-12 + 5e-13) / 2.0)


def test_permeability_tensor_invalid_direction():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    with pytest.raises(ValueError):
        tensor.effective_permeability_in_direction(direction='invalid')


def test_permeability_tensor_invalid_direction_vector_shape():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    with pytest.raises(ValueError):
        tensor.effective_permeability_in_direction(direction_vector=np.array([1, 0]))


def test_permeability_tensor_rotate():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    # Identity rotation → same tensor
    R_identity = np.eye(3)
    rotated = tensor.rotate(R_identity)
    assert isinstance(rotated, PermeabilityTensor)
    assert rotated.Kx == pytest.approx(tensor.Kx)
    assert rotated.Ky == pytest.approx(tensor.Ky)
    assert rotated.Kz == pytest.approx(tensor.Kz)

    # 90° rotation around z-axis → Kx and Ky swap
    theta = np.pi / 2
    R_z = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1],
    ])
    rotated = tensor.rotate(R_z)
    assert isinstance(rotated, PermeabilityTensor)
    assert rotated.Kx == pytest.approx(tensor.Ky)
    assert rotated.Ky == pytest.approx(tensor.Kx)
    assert rotated.Kz == pytest.approx(tensor.Kz)


def test_permeability_tensor_rotate_to_full_tensor():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    # 45° rotation around z-axis → off-diagonal components
    theta = np.pi / 4
    R_45 = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1],
    ])
    rotated = tensor.rotate(R_45)
    assert isinstance(rotated, FullTensor)


def test_permeability_tensor_to_dict():
    tensor = PermeabilityTensor(Kx=2e-12, Ky=1e-12, Kz=5e-13)
    d = tensor.to_dict()
    assert d['Kx'] == pytest.approx(2e-12)
    assert d['Ky'] == pytest.approx(1e-12)
    assert d['Kz'] == pytest.approx(5e-13)
    assert d['in_plane_average'] == pytest.approx(1.5e-12)
    assert 'anisotropy_ratio' in d
    assert 'degree_of_anisotropy' in d


def test_permeability_tensor_repr():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    rep = repr(tensor)
    assert "PermeabilityTensor(" in rep
    assert "Kx" in rep
    assert "Ky" in rep
    assert "Kz" in rep


# =============================================================================
# FullTensor - Full symmetric tensor
# =============================================================================


def test_full_tensor_construction():
    # 45° rotated diagonal tensor should give off-diagonal components
    R = np.array([
        [1, -1, 0],
        [1, 1, 0],
        [0, 0, 1],
    ]) / np.sqrt(2)
    K_diag = np.diag([1e-12, 5e-13, 1e-13])
    K_rotated = R @ K_diag @ R.T
    ft = FullTensor(K_rotated)
    np.testing.assert_array_equal(ft.matrix, (K_rotated + K_rotated.T) / 2)


def test_full_tensor_principal_values():
    K_diag = np.diag([1e-12, 5e-13, 1e-13])
    ft = FullTensor(K_diag)
    k1, k2, k3 = ft.principal_values
    assert k1 == pytest.approx(1e-12)
    assert k2 == pytest.approx(5e-13)
    assert k3 == pytest.approx(1e-13)


def test_full_tensor_principal_values_rotated():
    # Rotated tensor → eigenvalues should be same as original
    R = np.array([
        [1, -1, 0],
        [1, 1, 0],
        [0, 0, 1],
    ]) / np.sqrt(2)
    K_diag = np.diag([1e-12, 5e-13, 1e-13])
    K_rotated = R @ K_diag @ R.T
    ft = FullTensor(K_rotated)
    k1, k2, k3 = ft.principal_values
    assert k1 == pytest.approx(1e-12)
    assert k2 == pytest.approx(5e-13)
    assert k3 == pytest.approx(1e-13, rel=1e-3)


def test_full_tensor_to_principal_tensor():
    R = np.array([
        [1, -1, 0],
        [1, 1, 0],
        [0, 0, 1],
    ]) / np.sqrt(2)
    K_diag = np.diag([1e-12, 5e-13, 1e-13])
    K_rotated = R @ K_diag @ R.T
    ft = FullTensor(K_rotated)
    pt = ft.to_principal_tensor()
    assert isinstance(pt, PermeabilityTensor)
    assert pt.Kx == pytest.approx(1e-12)
    assert pt.Ky == pytest.approx(5e-13)
    assert pt.Kz == pytest.approx(1e-13, rel=1e-3)


def test_full_tensor_invalid_shape():
    with pytest.raises(ValueError):
        FullTensor(np.array([[1, 2], [3, 4]]))


def test_full_tensor_principal_directions():
    K_diag = np.diag([1e-12, 5e-13, 1e-13])
    ft = FullTensor(K_diag)
    eigvecs = ft.principal_directions
    assert eigvecs.shape == (3, 3)
    # Eigenvectors should be axis-aligned (each column is ± basis vector)
    # Note: eigh() returns eigenvalues/vectors in ascending order,
    # so column 0 → smallest eigenvalue (1e-13, z-dir), column 2 → largest (1e-12, x-dir)
    for i in range(3):
        # Each column should have exactly one non-zero element (±1)
        col = np.abs(eigvecs[:, i])
        assert sum(col > 0.5) == 1, f"Column {i} is not axis-aligned: {eigvecs[:, i]}"



# =============================================================================
# anisotropic_darcy_flux
# =============================================================================


def test_anisotropic_darcy_flux():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    grad_p = np.array([1000, 500, 100])
    mu = 0.192
    result = anisotropic_darcy_flux(tensor=tensor, grad_p=grad_p, mu=mu)

    expected_v = -(1.0 / mu) * (tensor.tensor @ grad_p)
    np.testing.assert_array_equal(result['darcy_velocity'], expected_v)

    expected_mag = np.linalg.norm(expected_v)
    assert result['flux_magnitude'] == pytest.approx(expected_mag)

    assert 'velocity_angle_from_gradP_deg' in result
    assert 'area_flux' not in result  # No area_normal provided


def test_anisotropic_darcy_flux_with_area_normal():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    grad_p = np.array([1000, 500, 100])
    mu = 0.192
    area_normal = np.array([1, 0, 0])
    result = anisotropic_darcy_flux(
        tensor=tensor, grad_p=grad_p, mu=mu, area_normal=area_normal
    )
    # area_flux = v · n
    expected_flux = np.dot(result['darcy_velocity'], area_normal)
    assert result['area_flux'] == pytest.approx(expected_flux)


def test_anisotropic_darcy_flux_isotropic():
    """In isotropic media, velocity should be anti-parallel to grad_p."""
    tensor = PermeabilityTensor.from_isotopic(K=1e-12)
    grad_p = np.array([1000, 0, 0])
    mu = 0.192
    result = anisotropic_darcy_flux(tensor=tensor, grad_p=grad_p, mu=mu)
    # Velocity should be in -x direction only
    assert result['darcy_velocity'][0] < 0
    assert result['darcy_velocity'][1] == pytest.approx(0, abs=1e-15)
    assert result['darcy_velocity'][2] == pytest.approx(0, abs=1e-15)
    # Angle should be 180° (exactly opposite direction)
    assert result['velocity_angle_from_gradP_deg'] == pytest.approx(180.0)



def test_anisotropic_darcy_flux_zero_grad_p():
    tensor = PermeabilityTensor(Kx=1e-12, Ky=5e-13, Kz=1e-13)
    grad_p = np.array([0, 0, 0])
    mu = 0.192
    result = anisotropic_darcy_flux(tensor=tensor, grad_p=grad_p, mu=mu)
    np.testing.assert_array_equal(result['darcy_velocity'], [0, 0, 0])
    assert result['flux_magnitude'] == pytest.approx(0)
    assert result['velocity_angle_from_gradP_deg'] == pytest.approx(0.0)


# =============================================================================
# anisotropy_evolution
# =============================================================================


def test_anisotropy_evolution_basic():
    """Test basic anisotropy evolution across PIP cycles."""
    K_data = np.array([
        [1.0e-12, 5.0e-13, 1.0e-13],   # Cycle 0
        [8.0e-13, 4.5e-13, 1.5e-13],   # Cycle 1
        [6.0e-13, 4.0e-13, 2.0e-13],   # Cycle 2
        [4.5e-13, 3.5e-13, 2.5e-13],   # Cycle 3
    ])
    cycles = np.array([0, 1, 2, 3])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    assert 'tensors' in result
    assert 'cycles' in result
    assert 'anisotropy_ratios' in result
    assert 'degrees_of_anisotropy' in result
    assert 'anisotropy_reduction' in result

    assert len(result['tensors']) == 4
    assert len(result['cycles']) == 4
    assert len(result['anisotropy_ratios']) == 4
    assert len(result['degrees_of_anisotropy']) == 4

    # Each tensor should be a PermeabilityTensor
    for tensor in result['tensors']:
        assert isinstance(tensor, PermeabilityTensor)

    # Cycles should match input
    np.testing.assert_array_equal(result['cycles'], cycles)


def test_anisotropy_evolution_anisotropy_ratios():
    """Test that anisotropy ratios decrease with densification."""
    K_data = np.array([
        [1.0e-12, 5.0e-13, 1.0e-13],   # Cycle 0: β = 7.5
        [8.0e-13, 4.5e-13, 1.5e-13],   # Cycle 1: β = 4.17
        [6.0e-13, 4.0e-13, 2.0e-13],   # Cycle 2: β = 2.5
        [4.5e-13, 3.5e-13, 2.5e-13],   # Cycle 3: β = 1.6
    ])
    cycles = np.array([0, 1, 2, 3])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    # Anisotropy ratios should strictly decrease
    for i in range(1, len(result['anisotropy_ratios'])):
        assert result['anisotropy_ratios'][i] < result['anisotropy_ratios'][i - 1]

    # Degrees of anisotropy should strictly decrease
    for i in range(1, len(result['degrees_of_anisotropy'])):
        assert result['degrees_of_anisotropy'][i] < result['degrees_of_anisotropy'][i - 1]


def test_anisotropy_evolution_ratios_values():
    """Test exact anisotropy ratio values."""
    K_data = np.array([
        [1.0e-12, 5.0e-13, 1.0e-13],  # Kx=1e-12, Ky=5e-13, Kz=1e-13
    ])
    cycles = np.array([0])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    # in_plane_average = (1e-12 + 5e-13) / 2 = 7.5e-13
    # β = 7.5e-13 / 1e-13 = 7.5
    expected_beta = 7.5
    assert result['anisotropy_ratios'][0] == pytest.approx(expected_beta)

    # δ = 1 - min/max = 1 - 1e-13/1e-12 = 0.9
    expected_delta = 0.9
    assert result['degrees_of_anisotropy'][0] == pytest.approx(expected_delta)


def test_anisotropy_evolution_reduction():
    """Test anisotropy reduction percentage."""
    K_data = np.array([
        [1.0e-12, 5.0e-13, 1.0e-13],   # Cycle 0: β = 7.5
        [4.5e-13, 3.5e-13, 2.5e-13],   # Cycle 3: β = 1.6
    ])
    cycles = np.array([0, 3])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    # Reduction = (β₀ - βₙ) / β₀ * 100
    beta_0 = 7.5
    beta_n = ((4.5e-13 + 3.5e-13) / 2) / 2.5e-13  # = 1.6
    expected_reduction = (beta_0 - beta_n) / beta_0 * 100
    assert result['anisotropy_reduction'] == pytest.approx(expected_reduction)


def test_anisotropy_evolution_isotropic_input():
    """Test evolution with isotropic permeability (should have β = 1, δ = 0)."""
    K_data = np.array([
        [1.0e-12, 1.0e-12, 1.0e-12],   # Fully isotropic
    ])
    cycles = np.array([0])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    assert result['anisotropy_ratios'][0] == pytest.approx(1.0)
    assert result['degrees_of_anisotropy'][0] == pytest.approx(0.0)


def test_anisotropy_evolution_single_cycle():
    """Test evolution with a single PIP cycle."""
    K_data = np.array([[1.0e-12, 5.0e-13, 1.0e-13]])
    cycles = np.array([0])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    assert len(result['tensors']) == 1
    assert result['anisotropy_reduction'] == pytest.approx(0.0)  # No change with single point


def test_anisotropy_evolution_invalid_input_shape():
    """Test that invalid input shapes raise errors."""
    with pytest.raises(ValueError):
        # Only Kx values, missing Ky and Kz
        anisotropy_evolution(
            K_values=np.array([[1e-12], [8e-13]]),
            cycles=np.array([0, 1])
        )


def test_anisotropy_evolution_tensor_objects():
    """Test that returned tensor objects store correct values."""
    K_data = np.array([
        [1.0e-12, 5.0e-13, 1.0e-13],
        [8.0e-13, 4.5e-13, 1.5e-13],
    ])
    cycles = np.array([0, 1])
    result = anisotropy_evolution(K_values=K_data, cycles=cycles)

    tensors = result['tensors']
    assert tensors[0].Kx == pytest.approx(1.0e-12)
    assert tensors[0].Ky == pytest.approx(5.0e-13)
    assert tensors[0].Kz == pytest.approx(1.0e-13)
    assert tensors[1].Kx == pytest.approx(8.0e-13)
    assert tensors[1].Ky == pytest.approx(4.5e-13)
    assert tensors[1].Kz == pytest.approx(1.5e-13)
