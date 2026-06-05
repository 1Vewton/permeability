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
from permeability.mcp.ProcessResult import (
    process_mcp_calculation_result
)
from permeability.mcp.Prompts import (
    mcp_instruction,
    permeability_calculation_instruction,
    infiltration_time_calculation_instruction,
    darcy2m2_instruction,
    m22darcy_instruction,
    infiltration_front_position_instruction,
    infiltration_front_position_multiple_time_instruction,
    capillary_pressure_calculation_instruction,
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
    r_meaning
)
from permeability.permeability.Seepage import (
    calculate_permeability,
    calculate_infiltration_time,
    calculate_infiltration_front_position,
    calculate_infiltration_front_position_with_multiple_time
)
from permeability.permeability.Capillary import (
    calculate_permeability_with_capillary_correction,
    calculate_infiltration_time_with_capillary_correction,
    calculate_infiltration_front_position_with_capillary_correction,
    calculate_infiltration_front_position_with_multiple_time_with_capillary_correction,
    calculate_capillary_pressure
)
from permeability.utils.UnitConverter import (
    darcy2m2,
    m22darcy
)


# mcp
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
    name="darcy_to_m2_converter",
    description=darcy2m2_instruction,
    tags={"permeability", "unit_converter"}
)
async def darcy_to_m2_converter(
        darcyK: Annotated[float, darcyK_meaning],
) -> dict:
    calculation_result = darcy2m2(darcyK=darcyK)
    return process_mcp_calculation_result(
        value=calculation_result,
        unit="m^2",
        meaning=m2K_meaning
    )


# Tool for converting m2 to darcy
@mcp.tool(
    name="m2_to_darcy_converter",
    description=m22darcy_instruction,
    tags={"permeability", "unit_converter"}
)
async def m2_to_darcy_converter(
        m2K: Annotated[float, m2K_meaning],
) -> dict:
    calculation_result = m22darcy(m2K=m2K)
    return process_mcp_calculation_result(
        value=calculation_result,
        unit="Darcy",
        meaning=darcyK_meaning
    )


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


# Run
def run():
    parser = argparse.ArgumentParser(description="My MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport")
    args = parser.parse_args()
    mcp.run(transport="http", host="localhost", port=args.port)
