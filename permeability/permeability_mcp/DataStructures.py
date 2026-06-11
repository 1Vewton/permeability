from typing import TypedDict, Annotated
from permeability.permeability_mcp.Prompts import (
    Kx_meaning,
    Ky_meaning,
    Kz_meaning,
    isotopic_K_meaning,
    K_in_plane_meaning,
    K_out_plane_meaning
)


# Build permeability tensor from principal values.
class PermeabilityTensorFromPrincipalValues(TypedDict):
    Kx: Annotated[float, Kx_meaning]
    Ky: Annotated[float, Ky_meaning]
    Kz: Annotated[float, Kz_meaning]


# Build permeability tensor from isotopic permeability.
class PermeabilityTensorFromIsotopicPermeability(TypedDict):
    K: Annotated[float, isotopic_K_meaning]


# Build permeability tensor from transversely isotopic permeability.
class PermeabilityTensorFromTransverselyIsotopicPermeabilityTensor(TypedDict):
    K_in_plane: Annotated[float, K_in_plane_meaning]
    K_out_plane: Annotated[float, K_out_plane_meaning]
