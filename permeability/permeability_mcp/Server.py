from typing import (
    Annotated,
    List,
    Optional
)
import argparse
import numpy as np
# Fastmcp dependencies
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
# Project dependencies
from permeability.permeability_mcp.ProcessResult import (
    process_mcp_calculation_result
)
from permeability.permeability_mcp.DataStructures import (
    PermeabilityTensorFromPrincipalValues,
    PermeabilityTensorFromIsotopicPermeability,
    PermeabilityTensorFromTransverselyIsotopicPermeabilityTensor
)
from permeability.permeability_mcp.Prompts import (
    mcp_instruction,
    permeability_calculation_instruction,
    infiltration_time_calculation_instruction,
    m2darcy_instruction,
    infiltration_front_position_instruction,
    infiltration_front_position_multiple_time_instruction,
    capillary_pressure_calculation_instruction,
    pressure_difference_calculation_instruction,
    anisotropic_darcy_flux_instruction,
    anisotropic_evolution_instruction,
    L_meaning,
    mu_meaning,
    phi_meaning,
    t_meaning,
    dP_meaning,
    K_meaning,
    multi_t_meaning,
    darcyK_meaning,
    m2K_meaning,
    z_meaning,
    p_c_meaning,
    gamma_meaning,
    theta_meaning,
    r_meaning,
    from_principal_value_meaning,
    from_isotopic_meaning,
    from_transversely_isotopic_meaning,
    grad_p_meaning,
    area_normal_meaning,
    K_values_meaning,
    cycles_meaning
)
from permeability.permeability.Seepage import (
    calculate_permeability,
    calculate_infiltration_time,
    calculate_infiltration_front_position,
    calculate_infiltration_front_position_with_multiple_time,
    calculate_pressure_difference
)
from permeability.permeability.Capillary import (
    calculate_permeability_with_capillary_correction,
    calculate_infiltration_time_with_capillary_correction,
    calculate_infiltration_front_position_with_capillary_correction,
    calculate_infiltration_front_position_with_multiple_time_with_capillary_correction,
    calculate_capillary_pressure,
    calculate_pressure_difference_with_capillary_correction
)
from permeability.permeability.AnisotropicTensor import (
    PermeabilityTensor,
    anisotropic_darcy_flux,
    anisotropy_evolution
)
from permeability.utils.UnitConverter import (
    darcy2m2,
    m22darcy
)


# permeability_mcp
mcp = FastMCP(
    "Permeability MCP",
    strict_input_validation=True,
    mask_error_details=True,
    instructions=mcp_instruction
)


# Calculate permeability
@mcp.tool(
    name="calculate_permeability_by_seepage_distance",
    description=permeability_calculation_instruction,
    tags={"permeability", "scalar_calculation"}
)
async def calculate_permeability_by_seepage_distance(
        L: Annotated[float, L_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        t: Annotated[float, t_meaning],
        dP: Annotated[float, dP_meaning],
        p_c: Optional[Annotated[float, p_c_meaning]] = None
) -> dict:
    try:
        if p_c is None:
            calculation_result = calculate_permeability(
                L=L,
                mu=mu,
                phi=phi,
                t=t,
                dP=dP
            )
        else:
            calculation_result = calculate_permeability_with_capillary_correction(
                L=L,
                mu=mu,
                phi=phi,
                t=t,
                dP=dP,
                p_c=p_c
            )
        return process_mcp_calculation_result(
            value=calculation_result,
            unit="m^2",
            meaning=K_meaning
        )
    except Exception as e:
        raise ToolError(e)


# Infiltration time calculation
@mcp.tool(
    name="calculate_infiltration_time",
    description=infiltration_time_calculation_instruction,
    tags={"permeability", "scalar_calculation"}
)
async def calculate_infiltration_time_tool(
        L: Annotated[float, L_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        K: Annotated[float, K_meaning],
        dP: Annotated[float, dP_meaning],
        p_c: Optional[Annotated[float, p_c_meaning]] = None
) -> dict:
    try:
        if p_c is None:
            calculation_result = calculate_infiltration_time(
                L=L,
                mu=mu,
                phi=phi,
                K=K,
                dP=dP
            )
        else:
            calculation_result = calculate_infiltration_time_with_capillary_correction(
                L=L,
                mu=mu,
                phi=phi,
                K=K,
                dP=dP,
                p_c=p_c
            )
        return process_mcp_calculation_result(
            value=calculation_result,
            unit="s",
            meaning=t_meaning
        )
    except Exception as e:
        raise ToolError(e)


# Tool for converting darcy to m2
@mcp.tool(
    name="darcy_m2_converter",
    description=m2darcy_instruction,
    tags={"permeability", "unit_converter"}
)
async def darcy_m2_converter(
        darcyK: Optional[Annotated[float, darcyK_meaning]] = None,
        m2K: Optional[Annotated[float, m2K_meaning]] = None,
) -> dict:
    result = {}
    if darcyK is not None:
        calculation_result = darcy2m2(darcyK=darcyK)
        result["darcy_converting_result"] = process_mcp_calculation_result(
            value=calculation_result,
            unit="m^2",
            meaning=m2K_meaning
        )
    if m2K is not None:
        calculation_result = m22darcy(m2K=m2K)
        result["m^2_converting_result"] = process_mcp_calculation_result(
            value=calculation_result,
            unit="Darcy",
            meaning=darcyK_meaning
        )
    return result


# Tool for calculating infiltration front position
@mcp.tool(
    name="calculate_infiltration_front_position",
    description=infiltration_front_position_instruction,
    tags={"permeability", "scalar_calculation"}
)
async def calculate_infiltration_front_position_tool(
        K: Annotated[float, K_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        dP: Annotated[float, dP_meaning],
        t: Annotated[float, t_meaning],
        p_c: Optional[Annotated[float, p_c_meaning]] = None
) -> dict:
    try:
        if p_c is None:
            calculation_result = calculate_infiltration_front_position(
                K=K,
                mu=mu,
                phi=phi,
                t=t,
                dP=dP
            )
        else:
            calculation_result = calculate_infiltration_front_position_with_capillary_correction(
                K=K,
                mu=mu,
                phi=phi,
                t=t,
                dP=dP,
                p_c=p_c
            )
        return process_mcp_calculation_result(
            value=calculation_result,
            unit="m",
            meaning=z_meaning
        )
    except Exception as e:
        raise ToolError(e)


# Tool for calculating infiltration front position for multiple time points
@mcp.tool(
    name="calculate_infiltration_front_position4multiple_times",
    description=infiltration_front_position_multiple_time_instruction,
    tags={"permeability", "graph_related", "vector_calculation"}
)
async def calculate_infiltration_front_position4multiple_times_tool(
    K: Annotated[float, K_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        dP: Annotated[float, dP_meaning],
        t: Annotated[List[float], multi_t_meaning],
        p_c: Optional[Annotated[float, p_c_meaning]] = None
) -> dict:
    try:
        processed_t = np.array(t)
        if p_c is None:
            calculation_result = calculate_infiltration_front_position_with_multiple_time(
                K=K,
                mu=mu,
                phi=phi,
                t=processed_t,
                dP=dP
            )
        else:
            calculation_result = (
                calculate_infiltration_front_position_with_multiple_time_with_capillary_correction(
                    K=K,
                    mu=mu,
                    phi=phi,
                    t=processed_t,
                    dP=dP,
                    p_c=p_c
                )
            )
        return process_mcp_calculation_result(
            value=calculation_result.tolist(),
            unit="m",
            meaning=z_meaning
        )
    except Exception as e:
        raise ToolError(e)


# Calculate capillary pressure
@mcp.tool(
    name="calculate_capillary_pressure",
    description=capillary_pressure_calculation_instruction,
    tags={"permeability", "scalar_calculation"}
)
async def calculate_capillary_pressure_tool(
        theta: Annotated[float, theta_meaning],
        r: Annotated[float, r_meaning],
        gamma: Annotated[float, gamma_meaning],
):
    try:
        calculation_result = calculate_capillary_pressure(
            theta=theta,
            r=r,
            gamma=gamma
        )
        return process_mcp_calculation_result(
            value=calculation_result,
            unit="Pa",
            meaning=p_c_meaning
        )
    except Exception as e:
        raise ToolError(e)


# Calculate pressure difference
@mcp.tool(
    name="calculate_pressure_difference",
    description=pressure_difference_calculation_instruction,
    tags={"permeability", "scalar_calculation"}
)
async def calculate_pressure_difference_tool(
        L: Annotated[float, L_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        K: Annotated[float, K_meaning],
        t: Annotated[float, t_meaning],
        p_c: Optional[Annotated[float, p_c_meaning]] = None,
):
    try:
        if p_c is None:
            calculation_result = calculate_pressure_difference(
                L=L,
                mu=mu,
                phi=phi,
                K=K,
                t=t
            )
        else:
            calculation_result = calculate_pressure_difference_with_capillary_correction(
                L=L,
                mu=mu,
                phi=phi,
                K=K,
                t=t,
                p_c=p_c
            )
        return process_mcp_calculation_result(
            value=calculation_result,
            unit="Pa",
            meaning=dP_meaning
        )
    except Exception as e:
        raise ToolError(e)


# Calculate darcy flux
@mcp.tool(
    name="calculate_darcy_flux_tool",
    description=anisotropic_darcy_flux_instruction,
    tags={"vector_calculation"}
)
async def calculate_darcy_flux_tool(
        grad_p: Annotated[List[float], grad_p_meaning],
        mu: Annotated[float, mu_meaning],
        area_normal: Optional[Annotated[List[float], area_normal_meaning]] = None,
        permeability_tensor_from_principal_value: Optional[
            Annotated[
                PermeabilityTensorFromPrincipalValues,
                from_principal_value_meaning,
            ]
        ] = None,
        permeability_tensor_from_isotopic: Optional[
            Annotated[
                PermeabilityTensorFromIsotopicPermeability,
                from_isotopic_meaning,
            ]
        ] = None,
        permeability_tensor_from_transversely_isotopic: Optional[
            Annotated[
                PermeabilityTensorFromTransverselyIsotopicPermeabilityTensor,
                from_transversely_isotopic_meaning,
            ]
        ] = None
):
    try:
        permeability_list = {}
        # Permeability tensor from principal value
        if permeability_tensor_from_principal_value is not None:
            permeability_list["tensor_constructed_from_principal_value"] = PermeabilityTensor.from_principal_values(
                Kx=permeability_tensor_from_principal_value.get("Kx"),
                Ky=permeability_tensor_from_principal_value.get("Ky"),
                Kz=permeability_tensor_from_principal_value.get("Kz"),
            )
        # Permeability tensor from isotopic permeability
        if permeability_tensor_from_isotopic is not None:
            permeability_list["tensor_constructed_from_isotopic"] = PermeabilityTensor.from_isotopic(
                K=permeability_tensor_from_isotopic.get("K"),
            )
        # Permeability tensor from transversely isotopic permeability
        if permeability_tensor_from_transversely_isotopic is not None:
            permeability_list["tensor_constructed_from_transversely_isotopic"] = (
                PermeabilityTensor.from_transversely_isotropic(
                    K_in_plane=permeability_tensor_from_transversely_isotopic.get("K_in_plane"),
                    K_out_plane=permeability_tensor_from_transversely_isotopic.get("K_out_plane"),
                )
            )
        # Collect the result
        result = {}
        for i in permeability_list.keys():
            result[i] = anisotropic_darcy_flux(
                permeability_list[i],
                grad_p=np.array(grad_p),
                mu=mu,
                area_normal=area_normal,
            )
        return result
    except Exception as e:
        raise ToolError(e)


# Calculate the anisotropy evolution
@mcp.tool(
    name="calculate_anisotropy_evolution_tool",
    description=anisotropic_evolution_instruction,
    tags={"vector_calculation"}
)
async def calculate_anisotropy_evolution_tool(
        K_values: Annotated[List[float], K_values_meaning],
        cycles: Annotated[List[float], cycles_meaning],
):
    try:
        result = anisotropy_evolution(
            np.array(K_values),
            np.array(cycles),
        )
        return result
    except Exception as e:
        raise ToolError(e)


# Run
def run():
    parser = argparse.ArgumentParser(description="My MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport")
    args = parser.parse_args()
    mcp.run(transport="http", host="localhost", port=args.port)
