def process_mcp_calculation_result(
        value: float,
        unit: str,
        meaning: str,
) -> dict:
    return {
        "val": value,
        "unit": unit,
        "meaning": meaning,
    }
