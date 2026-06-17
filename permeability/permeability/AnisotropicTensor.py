import numpy as np
from typing import Tuple, Optional


class PermeabilityTensor:
    '''
    Anisotropic permeability tensor for 2D woven composites.
    Represents the diagonal permeability tensor:
    K = diag(Kx, Ky, Kz)
    '''

    def __init__(
            self,
            Kx,
            Ky,
            Kz,
    ):
        '''
        Initialize the permeability tensor
        :param Kx: Permeability in x-direction (warp/fiber direction) [m²]
        :param Ky: Permeability in y-direction (weft direction) [m²]
        :param Kz: Permeability in z-direction (through-thickness) [m²]
        '''
        self.Kx = Kx
        self.Ky = Ky
        self.Kz = Kz
        if self.Kx <= 0:
            raise ValueError("Kx must be positive")
        if self.Ky <= 0:
            raise ValueError("Ky must be positive")
        if self.Kz <= 0:
            raise ValueError("Kz must be positive")

    @classmethod
    def from_principal_values(
            cls,
            Kx: float,
            Ky: float,
            Kz: float,
    ):
        """
        Construct tensor from principal direction permeabilities.

        This is the standard constructor for orthotropic materials
        where principal axes align with the coordinate system.
        :param Kx: Permeability in x-direction (warp/fiber direction) [m²]
        :param Ky: Permeability in y-direction (weft direction) [m²]
        :param Kz: Permeability in z-direction (through-thickness) [m²]
        :return: Permeability Tensor
        """
        return cls(
            Kx=Kx,
            Ky=Ky,
            Kz=Kz,
        )

    @classmethod
    def from_isotopic(
            cls,
            K: float
    ):
        """
        Construct an isotropic permeability tensor.

        Kx = Ky = Kz = K
        :param K: Isotropic permeability [m²]
        :return: Permeability Tensor
        """
        return cls(Kx=K, Ky=K, Kz=K)

    @classmethod
    def from_transversely_isotropic(
            cls,
            K_in_plane: float,
            K_out_plane: float
    ):
        """
        Construct a transversely isotropic permeability tensor.

        Kx = Ky = K_in_plane
        Kz = K_out_plane

        This model is appropriate for unidirectional fiber bundles.
        :param K_in_plain: In-plane permeability (x and y directions) [m²]
        :param K_out_plane: Out-of-plane permeability (z direction) [m²]
        :return: Permeability Tensor
        """
        return cls(Kx=K_in_plane, Ky=K_in_plane, Kz=K_out_plane)

    @property
    def tensor(self) -> np.ndarray:
        """
        :return: the full 3x3 diagonal tensor matrix.
        """
        return np.diag([self.Kx, self.Ky, self.Kz])

    @property
    def in_plane_average(self) -> float:
        """
        :return: Average in-plane permeability (Kx + Ky) / 2.
        """
        return (self.Kx + self.Ky) / 2

    @property
    def anisotropy_ratio(self) -> float:
        """
        :return: Anisotropy ratio. β >> 1 indicates strong anisotropy.
        """
        return self.in_plane_average / self.Kz

    @property
    def degree_of_anisotropy(self) -> float:
        """
        :return: Degree of anisotropy (0 = isotropic, 1 = fully anisotropic).
        """
        K_max = max(self.Kx, self.Ky, self.Kz)
        K_min = min(self.Kx, self.Ky, self.Kz)
        return 1.0 - K_min / K_max

    def rotate(self, R: np.ndarray):
        """
        Rotate the permeability tensor by rotation matrix R.

        K' = R · K · R^T  [Eq. 4.18]
        :param R: Orthogonal rotation matrix (R^{-1} = R^T)
        :return:
        """
        K_rotated = R @ self.tensor @ R.T
        # Check if off-diagonal terms are negligible
        off_diag = np.sqrt(
            K_rotated[0, 1] ** 2 + K_rotated[0, 2] ** 2 + K_rotated[1, 2] ** 2
        )
        diag_norm = np.linalg.norm(np.diag(K_rotated))

        if off_diag / (diag_norm + 1e-30) < 1e-10:
            # Off-diagonal terms are negligible → return diagonal tensor
            return PermeabilityTensor(
                Kx=K_rotated[0, 0],
                Ky=K_rotated[1, 1],
                Kz=K_rotated[2, 2]
            )
        else:
            return FullTensor.from_matrix(K_rotated)

    def darcy_velocity(
        self,
        grad_p: np.ndarray,
        mu: float
    ) -> np.ndarray:
        """
        Calculate Darcy velocity vector.

        v = -(1/μ) · K · ∇p
        :param grad_p: Pressure gradient vector [Pa/m]
        :param mu: Dynamic viscosity [Pa·s]
        :return: Darcy velocity vector [m/s]
        """
        if mu <= 0.0:
            raise ValueError("mu must be greater than 0")
        return -(1.0 / mu) * (self.tensor @ grad_p)

    def effective_permeability_in_direction(
            self,
            direction: Optional[str] = None,
            direction_vector: Optional[np.ndarray] = None
    ):
        """
        Calculate effective permeability in an arbitrary direction.

        For a direction unit vector n, the effective permeability is:
        K_eff = n^T · K · n
        :param direction: one of 'x', 'y', 'z', 'xy' (in-plane), 'avg'
        :param direction_vector: Unit vector of shape (3,)
        :return: Effective permeability in the specified direction [m²]
        """
        if direction is not None:
            direction = direction.lower()
            if direction == 'x':
                return self.Kx
            elif direction == 'y':
                return self.Ky
            elif direction == 'z':
                return self.Kz
            elif direction in ('xy', 'in_plane', 'in-plane'):
                return self.in_plane_average
            elif direction == 'avg':
                return (self.Kx + self.Ky + self.Kz) / 3.0
            else:
                raise ValueError(
                    f"Unknown direction: {direction}. "
                    "Use: 'x', 'y', 'z', 'xy', or 'avg'."
                )
        else:
            # Arbitrary direction given by unit vector
            n = np.asarray(direction_vector)
            if n.shape != (3,):
                raise ValueError(f"Direction vector must be shape (3,), got {n.shape}")
            norm = np.linalg.norm(n)
            if abs(norm - 1.0) > 1e-10:
                n = n / norm  # Normalize
            return n @ self.tensor @ n

    def to_dict(self) -> dict:
        """Export tensor data as a dictionary."""
        return {
            'Kx': self.Kx,
            'Ky': self.Ky,
            'Kz': self.Kz,
            'in_plane_average': self.in_plane_average,
            'anisotropy_ratio': self.anisotropy_ratio,
            'degree_of_anisotropy': self.degree_of_anisotropy
        }

    def __repr__(self) -> str:
        K_avg = (self.Kx + self.Ky + self.Kz) / 3.0
        return (
            f"PermeabilityTensor(\n"
            f"  Kx = {self.Kx:.4e} m²\n"
            f"  Ky = {self.Ky:.4e} m²\n"
            f"  Kz = {self.Kz:.4e} m²\n"
            f"  K_avg = {K_avg:.4e} m²\n"
            f"  β (anisotropy ratio) = {self.anisotropy_ratio:.2f}\n"
            f")"
        )


class FullTensor:
    """
    Full 3x3 symmetric permeability tensor with off-diagonal components.

    Used after coordinate rotation when the tensor is no longer diagonal.
    """

    def __init__(self, matrix: np.ndarray):
        """
        Initialize the full 3x3 symmetric permeability tensor
        :param matrix:
        """
        self.matrix = matrix
        if self.matrix.shape != (3, 3):
            raise ValueError(f"Matrix must be shape (3, 3), got {self.matrix.shape}")
        self.matrix = (self.matrix.T + self.matrix)/2

    @classmethod
    def from_matrix(cls, matrix: np.ndarray):
        """
        Construct full 3x3 symmetric permeability tensor
        :param matrix: the matrix
        """
        return cls(matrix=matrix.copy())

    @property
    def principal_values(self) -> Tuple[float, float, float]:
        """
        Compute principal permeability values (eigenvalues).
        :return: (K1, K2, K3) where K1 >= K2 >= K3
        """
        eigenvalues = np.linalg.eigvalsh(self.matrix)
        # In descending order
        return (eigenvalues[2], eigenvalues[1], eigenvalues[0])

    @property
    def principal_directions(self) -> np.ndarray:
        """
        Compute principal permeability directions (eigenvectors).
        """
        eigenvalues, eigenvectors = np.linalg.eigh(self.matrix)
        # eigenvectors[:, 0] corresponds to smallest eigenvalue
        return eigenvectors

    def to_principal_tensor(self) -> PermeabilityTensor:
        """
        Convert to diagonal tensor in principal coordinate system.
        :return: Diagonal tensor with principal permeability values.
        """
        K1, K2, K3 = self.principal_values
        return PermeabilityTensor(Kx=K1, Ky=K2, Kz=K3)


def anisotropic_darcy_flux(
    tensor: PermeabilityTensor,
    grad_p: np.ndarray,
    mu: float,
    area_normal: Optional[np.ndarray] = None
) -> dict:
    """
    Compute Darcy flux and related quantities for anisotropic media.
    :param tensor: Anisotropic permeability tensor
    :param grad_p: Pressure gradient vector [Pa/m]
    :param mu: Dynamic viscosity [Pa·s]
    :param area_normal: Unit normal vector of the cross-section area.
                        If provided, computes the flux through that specific plane.
    :return: Contains 'darcy_velocity' (m/s), 'flux_magnitude' (m/s),
             'velocity_angle' (deg from pressure gradient direction),
              and optionally 'area_flux' (m³/s per m² of given area).
    """
    # Darcy velocity: v = -(1/μ) · K · ∇p
    v = tensor.darcy_velocity(grad_p, mu)
    v_mag = np.linalg.norm(v)

    # Angle between velocity and pressure gradient
    grad_p_norm = np.linalg.norm(grad_p)
    if grad_p_norm > 0:
        cos_angle = np.dot(v, grad_p) / (v_mag * grad_p_norm)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle_deg = np.degrees(np.arccos(cos_angle))
    else:
        angle_deg = 0.0

    result = {
        'darcy_velocity': v,
        'flux_magnitude': v_mag,
        'velocity_angle_from_gradP_deg': angle_deg
    }

    # If area normal is specified, compute flux through that plane
    if area_normal is not None:
        n = np.asarray(area_normal)
        n = n / np.linalg.norm(n)
        area_flux = np.dot(v, n)  # v · n: volumetric flux per unit area
        result['area_flux'] = area_flux

    return result


def anisotropy_evolution(
        K_values: np.ndarray,
        cycles: np.ndarray
) -> dict:
    """
    Analyze the evolution of permeability anisotropy across PIP cycles.
    :param K_values: Each row is [Kx, Ky, Kz] for one PIP cycle
    :param cycles: PIP cycle numbers
    :return: Contains tensors, anisotropy ratios, and cycle-by-cycle data
    """
    if K_values.ndim != 2 or K_values.shape[1] != 3:
        raise ValueError(
            f"K_values must be a 2D array of shape (n, 3), got shape {K_values.shape}"
        )
    if len(cycles) != K_values.shape[0]:
        raise ValueError(
            f"cycles length ({len(cycles)}) must match K_values rows ({K_values.shape[0]})"
        )
    n = len(cycles)
    tensors = []
    betas = np.zeros(n)
    das = np.zeros(n)

    for i in range(n):
        tensor = PermeabilityTensor(
            Kx=K_values[i, 0],
            Ky=K_values[i, 1],
            Kz=K_values[i, 2]
        )
        tensors.append(tensor)
        betas[i] = tensor.anisotropy_ratio
        das[i] = tensor.degree_of_anisotropy

    return {
        'tensors': tensors,
        'cycles': cycles,
        'anisotropy_ratios': betas,
        'degrees_of_anisotropy': das,
        'anisotropy_reduction': (betas[0] - betas[-1]) / betas[0] * 100
    }
