import numpy as np
from typing import Tuple


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
