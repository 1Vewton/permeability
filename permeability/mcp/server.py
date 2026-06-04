from typing import Annotated
import argparse
# Fastmcp dependencies
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
# Project dependencies
from permeability.mcp.prompts import (
    mcp_instruction,
    permeability_calculation_instruction,
    infiltration_time_calculation_instruction,
    L_meaning,
    mu_meaning,
    phi_meaning,
    t_meaning,
    dP_meaning,
    K_meaning
)
from permeability.permeability.SeepageDistance import (
    calculate_permeability,
    calculate_infiltration_time
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
    tags={"permeability", "calculation"}
)
async def calculate_permeability_by_seepage_distance(
        L: Annotated[float, L_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        t: Annotated[float, t_meaning],
        dP: Annotated[float, dP_meaning],
) -> Annotated[float, K_meaning]:
    try:
        calculation_result = calculate_permeability(
            L=L,
            mu=mu,
            phi=phi,
            t=t,
            dP=dP
        )
        return calculation_result
    except Exception as e:
        raise ToolError(e)


# Infiltration time calculation
@mcp.tool(
    name="calculate_infiltration_time",
    description=infiltration_time_calculation_instruction,
    tags={"permeability", "calculation"}
)
async def calculate_infiltration_time_tool(
        L: Annotated[float, L_meaning],
        mu: Annotated[float, mu_meaning],
        phi: Annotated[float, phi_meaning],
        K: Annotated[float, K_meaning],
        dP: Annotated[float, dP_meaning],
) -> Annotated[float, t_meaning]:
    try:
        calculation_result = calculate_infiltration_time(
            L=L,
            mu=mu,
            phi=phi,
            K=K,
            dP=dP
        )
        return calculation_result
    except Exception as e:
        raise ToolError(e)


# Run
def run():
    parser = argparse.ArgumentParser(description="My MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport")
    args = parser.parse_args()
    mcp.run(transport="http", host="localhost", port=args.port)
