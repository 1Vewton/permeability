# permeability

A Python package for calculating permeability of porous media using the **seepage distance method**, derived from the Darcy's law-based formula:

$$
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot \Delta P}
$$

$$
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot \Delta P}
$$

| Symbol | Meaning | Unit |
|--------|---------|------|
| $K$ | Permeability | m² |
| $L$ | Sample thickness along flow direction | m |
| $\mu$ | Dynamic viscosity of fluid | Pa·s |
| $\phi$ | Porosity of porous medium | dimensionless |
| $t$ | Time for fluid to fully penetrate sample | s |
| $\Delta P$ | Constant pressure difference across sample | Pa |
| $z$ | Infiltration front position | m |

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
from permeability.permeability import Seepage

# Experimental parameters
K = Seepage.calculate_permeability(
    L=0.003,   # Sample thickness: 3 mm
    mu=0.192,  # Fluid viscosity: 0.192 Pa·s
    phi=0.445, # Porosity: 0.445
    t=100,     # Penetration time: 100 s
    dP=1e4     # Pressure difference: 10,000 Pa
)
print(f"Permeability: {K:.3e} m²")  # ~3.84e-13 m²
```

### Predict Infiltration Time

```python
t = Seepage.calculate_infiltration_time(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    dP=1e4
)
print(f"Infiltration time: {t:.2f} s")  # ~100.00 s
```

### Calculate Infiltration Front Position

```python
# Single time point
z = Seepage.calculate_infiltration_front_position(
    K=1.284e-13,
    mu=0.192,
    phi=0.642,
    dP=1e5,
    t=120
)
print(f"Front position: {z:.4f} m")  # ~0.0050 m

# Multiple time points (for graphing)
import numpy as np
z_array = Seepage.calculate_infiltration_front_position_with_multiple_time(
    K=1.284e-13,
    mu=0.192,
    phi=0.642,
    dP=1e5,
    t=np.array([0, 30, 120])
)
print(f"Front positions: {z_array}")  # [0.0, 0.0025, 0.005]
```

### Unit Conversion

```python
from permeability.utils.UnitConverter import darcy2m2, m22darcy

# Convert m² to Darcy
darcy = m22darcy(m2K=3.8448e-13)
print(f"Permeability: {darcy:.3f} Darcy")  # ~0.390 Darcy

# Convert Darcy to m²
m2 = darcy2m2(darcyK=0.3896)
print(f"Permeability: {m2:.3e} m²")  # ~3.845e-13 m²
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
| `calculate_permeability_by_seepage_distance` | Calculate $K = L^2 \cdot \mu \cdot \phi \,/\, (2 \cdot t \cdot \Delta P)$ |
| `calculate_infiltration_time` | Calculate $t = \mu \cdot \phi \cdot L^2 \,/\, (2 \cdot K \cdot \Delta P)$ |
| `calculate_infiltration_front_position` | Calculate $z(t) = \sqrt{2 \cdot K \cdot \Delta P \cdot t \,/\, (\mu \cdot \phi)}$ |
| `calculate_infiltration_front_position4multiple_times` | Calculate $z(t)$ for multiple time points (for graphing) |
| `darcy_to_m2_converter` | Convert Darcy to m² |
| `m2_to_darcy_converter` | Convert m² to Darcy |

Each tool accepts the same parameters as the Python API.

---

## API Reference

### `Seepage.calculate_permeability(L, mu, phi, t, dP)`

Calculate permeability from seepage distance experiment data.

$$
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot \Delta P}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `t` | float | Total time for fluid to fully penetrate sample (s) |
| `dP` | float | Constant pressure difference across sample (Pa) |

**Returns:** `float` — Permeability $K$ (m²)

---

### `Seepage.calculate_infiltration_time(L, mu, phi, K, dP)`

Predict the time required for fluid to fully penetrate a sample.

$$
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot \Delta P}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `K` | float | Permeability (m²) |
| `dP` | float | Constant pressure difference across sample (Pa) |

**Returns:** `float` — Infiltration time $t$ (s)

---

### `Seepage.calculate_infiltration_front_position(K, mu, phi, dP, t)`

Calculate the infiltration front position at a given time.

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `K` | float | Permeability (m²) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `dP` | float | Constant pressure difference across sample (Pa) |
| `t` | float | Time elapsed (s) |

**Returns:** `float` — Infiltration front position $z$ (m)

---

### `Seepage.calculate_infiltration_front_position_with_multiple_time(K, mu, phi, dP, t)`

Calculate the infiltration front position at multiple time points (useful for plotting).

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `K` | float | Permeability (m²) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `dP` | float | Constant pressure difference across sample (Pa) |
| `t` | numpy.ndarray | Array of time values (s) |

**Returns:** `numpy.ndarray` — Array of infiltration front positions $z$ (m)

---

### `darcy2m2(darcyK)`

Convert permeability from Darcy to m².

| Parameter | Type | Description |
|-----------|------|-------------|
| `darcyK` | float | Permeability in Darcy |

**Returns:** `float` — Permeability in m²

---

### `m22darcy(m2K)`

Convert permeability from m² to Darcy.

| Parameter | Type | Description |
|-----------|------|-------------|
| `m2K` | float | Permeability in m² |

**Returns:** `float` — Permeability in Darcy

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
