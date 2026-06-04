# permeability

A Python package for calculating permeability of porous media using the **seepage distance method**, derived from the Darcy's law-based formula:

```
K = L² · μ · φ / (2 · t · ΔP)
t = μ · φ · L² / (2 · K · ΔP)
```

| Symbol | Meaning | Unit |
|--------|---------|------|
| K | Permeability | m² |
| L | Sample thickness along flow direction | m |
| μ | Dynamic viscosity of fluid | Pa·s |
| φ | Porosity of porous medium | dimensionless |
| t | Time for fluid to fully penetrate sample | s |
| ΔP | Constant pressure difference across sample | Pa |

This package also provides an **MCP server** that exposes these calculations as tools for AI assistants like Claude.

---

## Installation

### Using pip

```bash
pip install permeability
```

### Using uv (recommended)

```bash
uv add permeability
```

---

## Quick Start

### Calculate Permeability from Experimental Data

```python
from permeability.permeability import SeepageDistance

# Experimental parameters
K = SeepageDistance.calculate_permeability(
    L=0.003,    # Sample thickness: 3 mm
    mu=0.192,   # Fluid viscosity: 0.192 Pa·s
    phi=0.445,  # Porosity: 0.445
    t=100,      # Penetration time: 100 s
    dP=1e4      # Pressure difference: 10,000 Pa
)
print(f"Permeability: {K:.3e} m²")  # ~3.84e-13 m²
```

### Predict Infiltration Time

```python
t = SeepageDistance.calculate_infiltration_time(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    dP=1e4
)
print(f"Infiltration time: {t:.2f} s")  # ~100.00 s
```

---

## MCP Server

The package includes a **Model Context Protocol (MCP) server** that exposes permeability calculations as AI-accessible tools.

### Starting the Server

#### Option 1: Using uv (no installation required)

```bash
# Default port 8000
uv run permeability_mcp

# Custom port
uv run permeability_mcp --port 8080
```

This starts the server via HTTP/SSE transport (`http://localhost:8000` by default).

#### Option 2: After installation

```bash
# Default port 8000
permeability_mcp

# Custom port
permeability_mcp --port 8080
```

### MCP Configuration for AI Assistants

#### For **Claude Desktop**, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "permeability": {
      "command": "uv",
      "args": ["run", "permeability_mcp", "--port", "8080"]
    }
  }
}
```

#### For **Cline (VS Code extension)**, add to your MCP settings:

```json
{
  "mcpServers": {
    "permeability": {
      "command": "uv",
      "args": ["run", "permeability_mcp", "--port", "8080"]
    }
  }
}
```

### Available Tools

Once the MCP server is running, AI assistants can call:

| Tool | Description |
|------|-------------|
| `calculate_permeability_by_seepage_distance` | Calculate K = L²·μ·φ / (2·t·ΔP) |
| `calculate_infiltration_time` | Calculate t = μ·φ·L² / (2·K·ΔP) |

Each tool accepts the same parameters as the Python API.

---

## API Reference

### `SeepageDistance.calculate_permeability(L, mu, phi, t, dP)`

Calculate permeability from seepage distance experiment data.

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium (0 < φ ≤ 1) |
| `t` | float | Total time for fluid to fully penetrate sample (s) |
| `dP` | float | Constant pressure difference across sample (Pa) |

**Returns:** `float` — Permeability K (m²)

### `SeepageDistance.calculate_infiltration_time(L, mu, phi, K, dP)`

Predict the time required for fluid to fully penetrate a sample.

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium (0 < φ ≤ 1) |
| `K` | float | Permeability (m²) |
| `dP` | float | Constant pressure difference across sample (Pa) |

**Returns:** `float` — Infiltration time t (s)

---

## Development

### Setup

```bash
git clone https://github.com/1Vewton/permeability.git
cd permeability
uv sync
```

### Running Tests

```bash
uv run pytest
```

### Code Style

```bash
uv run flake8
```

---

## License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.
