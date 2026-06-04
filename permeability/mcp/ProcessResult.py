from typing import Any


# Process result for calculation
def process_mcp_calculation_result(
        value: Any,
        unit: str,
        meaning: str,
) -> dict:
    return {
        "val": value,
        "unit": unit,
        "meaning": meaning,
    }
