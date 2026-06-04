from typing import Annotated
import argparse
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
    L_meaning,
    mu_meaning,
    phi_meaning,
    t_meaning,
    dP_meaning,
    K_meaning,
    darcyK_meaning,
    m2K_meaning
)
from permeability.permeability.SeepageDistance import (
    calculate_permeability,
    calculate_infiltration_time
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
) -> dict:
    try:
        calculation_result = calculate_permeability(
            L=L,
            mu=mu,
            phi=phi,
            t=t,
            dP=dP
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
) -> dict:
    try:
        calculation_result = calculate_infiltration_time(
            L=L,
            mu=mu,
            phi=phi,
            K=K,
            dP=dP
        )
        return process_mcp_calculation_result(
            value=calculation_result,
            unit="s",
            meaning=t_meaning
        )
    except Exception as e:
        raise ToolError(e)


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


# Run
def run():
    parser = argparse.ArgumentParser(description="My MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport")
    args = parser.parse_args()
    mcp.run(transport="http", host="localhost", port=args.port)
