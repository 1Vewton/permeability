# permeability

A Python package for calculating permeability of porous media using the **seepage distance method**, derived from the Darcy's law-based formula, with **capillary pressure correction** via the Young-Laplace equation:

$$
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot \Delta P}
$$

$$
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot \Delta P}
$$

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
$$

$$
p_c = \frac{2 \cdot \gamma \cdot \cos(\theta)}{r}
$$

### Capillary-Corrected Forms

When capillary pressure $p_c$ is considered, $\Delta P$ is replaced by $(\Delta P + p_c)$:

$$
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot (\Delta P + p_c)}
$$

$$
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot (\Delta P + p_c)}
$$

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot (\Delta P + p_c) \cdot t}{\mu \cdot \phi}}
$$

$$
\Delta P = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot t}
$$

$$
\Delta P = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot t} - p_c
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
| $p_c$ | Capillary pressure | Pa |
| $\gamma$ | Surface tension of the liquid | N/m |
| $\theta$ | Contact angle (wetting angle) | Degrees |
| $r$ | Equivalent pore radius | m |

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

### Calculate Capillary Pressure

```python
from permeability.permeability.Capillary import calculate_capillary_pressure

# Capillary pressure via Young-Laplace equation
p_c = calculate_capillary_pressure(
    gamma=0.072,  # Surface tension of water: 0.072 N/m
    theta=30,     # Contact angle: 30 degrees
    r=1e-6        # Pore radius: 1 µm
)
print(f"Capillary pressure: {p_c:.2f} Pa")  # ~124.71 Pa
```

### Permeability with Capillary Correction

```python
# Calculate permeability considering capillary pressure
K_corrected = Seepage.calculate_permeability(
    L=0.003,
    mu=0.192,
    phi=0.445,
    t=100,
    dP=1e4,
    p_c=124.71  # Capillary pressure (Pa)
)
print(f"Corrected permeability: {K_corrected:.3e} m²")
```

### Calculate Pressure Difference

```python
# Calculate the pressure difference applied across the sample
dP = Seepage.calculate_pressure_difference(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    t=100
)
print(f"Pressure difference: {dP:.2f} Pa")  # ~10000.00 Pa

# With capillary correction
dP_corrected = Seepage.calculate_pressure_difference(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    t=100,
    p_c=124.71  # Capillary pressure (Pa)
)
print(f"Corrected pressure difference: {dP_corrected:.2f} Pa")
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

The package includes a **Model Context Protocol (MCP) server** that exposes permeability calculations as AI-accessible tools. After [installing the package](#installation), start the server with:

### Starting the Server

Once installed, simply run:

```bash
# Default port 8000
permeability_mcp

# Custom port
permeability_mcp --port 8080
```

The server starts via HTTP/SSE transport (`http://localhost:8000` by default).

If you prefer to try it without installing, you can also use:

```bash
uvx --from permeability permeability_mcp
```

### Configuration for AI Assistants

#### For **Claude Desktop**, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "permeability": {
      "command": "permeability_mcp",
      "args": ["--port", "8080"]
    }
  }
}
```

#### For **Cline (VS Code extension)**, add to your MCP settings:

```json
{
  "mcpServers": {
    "permeability": {
      "command": "permeability_mcp",
      "args": ["--port", "8080"]
    }
  }
}
```

### Available Tools

Once the MCP server is running, AI assistants can call:

| Tool | Description |
|------|-------------|
| `calculate_permeability_by_seepage_distance` | Calculate $K$ (optionally with capillary correction via $p_c$) |
| `calculate_infiltration_time` | Calculate $t$ (optionally with capillary correction via $p_c$) |
| `calculate_infiltration_front_position` | Calculate $z(t)$ (optionally with capillary correction via $p_c$) |
| `calculate_infiltration_front_position4multiple_times` | Calculate $z(t)$ for multiple time points (optionally with capillary correction via $p_c$) |
| `calculate_capillary_pressure` | Calculate $p_c = 2\gamma\cos(\theta)\,/\,r$ (Young-Laplace equation) |
| `calculate_pressure_difference` | Calculate $\Delta P$ (optionally with capillary correction via $p_c$) |
| `darcy_to_m2_converter` | Convert Darcy to m² |
| `m2_to_darcy_converter` | Convert m² to Darcy |

Each tool accepts the same parameters as the Python API.

---

## API Reference

### `Seepage.calculate_permeability(L, mu, phi, t, dP, p_c=None)`

Calculate permeability from seepage distance experiment data. When $p_c$ is provided, the capillary-corrected form is used.

$$
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot \Delta P}
\qquad\text{or}\qquad
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot (\Delta P + p_c)}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `t` | float | Total time for fluid to fully penetrate sample (s) |
| `dP` | float | Constant pressure difference across sample (Pa) |
| `p_c` | float, optional | Capillary pressure for correction (Pa) |

**Returns:** `float` — Permeability $K$ (m²)

---

### `Seepage.calculate_infiltration_time(L, mu, phi, K, dP, p_c=None)`

Predict the time required for fluid to fully penetrate a sample. When $p_c$ is provided, the capillary-corrected form is used.

$$
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot \Delta P}
\qquad\text{or}\qquad
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot (\Delta P + p_c)}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `K` | float | Permeability (m²) |
| `dP` | float | Constant pressure difference across sample (Pa) |
| `p_c` | float, optional | Capillary pressure for correction (Pa) |

**Returns:** `float` — Infiltration time $t$ (s)

---

### `Seepage.calculate_infiltration_front_position(K, mu, phi, dP, t, p_c=None)`

Calculate the infiltration front position at a given time. When $p_c$ is provided, the capillary-corrected form is used.

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
\qquad\text{or}\qquad
z(t) = \sqrt{\frac{2 \cdot K \cdot (\Delta P + p_c) \cdot t}{\mu \cdot \phi}}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `K` | float | Permeability (m²) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `dP` | float | Constant pressure difference across sample (Pa) |
| `t` | float | Time elapsed (s) |
| `p_c` | float, optional | Capillary pressure for correction (Pa) |

**Returns:** `float` — Infiltration front position $z$ (m)

---

### `Seepage.calculate_infiltration_front_position_with_multiple_time(K, mu, phi, dP, t, p_c=None)`

Calculate the infiltration front position at multiple time points (useful for plotting). When $p_c$ is provided, the capillary-corrected form is used.

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
\qquad\text{or}\qquad
z(t) = \sqrt{\frac{2 \cdot K \cdot (\Delta P + p_c) \cdot t}{\mu \cdot \phi}}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `K` | float | Permeability (m²) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `dP` | float | Constant pressure difference across sample (Pa) |
| `t` | numpy.ndarray | Array of time values (s) |
| `p_c` | float, optional | Capillary pressure for correction (Pa) |

**Returns:** `numpy.ndarray` — Array of infiltration front positions $z$ (m)

---

### `Seepage.calculate_pressure_difference(L, mu, phi, K, t, p_c=None)`

Calculate the pressure difference across a sample. When $p_c$ is provided, the capillary-corrected form is used.

$$
\Delta P = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot t}
\qquad\text{or}\qquad
\Delta P = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot t} - p_c
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `L` | float | Sample length/thickness along flow direction (m) |
| `mu` | float | Dynamic viscosity of fluid (Pa·s) |
| `phi` | float | Porosity of porous medium ($0 < \phi \le 1$) |
| `K` | float | Permeability (m²) |
| `t` | float | Total time for fluid to fully penetrate sample (s) |
| `p_c` | float, optional | Capillary pressure for correction (Pa) |

**Returns:** `float` — Pressure difference $\Delta P$ (Pa)

---

### `calculate_capillary_pressure(gamma, theta, r)`

Calculate capillary pressure using the **Young-Laplace equation**.

$$
p_c = \frac{2 \cdot \gamma \cdot \cos(\theta)}{r}
$$

| Parameter | Type | Description |
|-----------|------|-------------|
| `gamma` | float | Surface tension of the liquid (N/m) |
| `theta` | float | Contact angle / wetting angle (Degrees) |
| `r` | float | Equivalent pore radius (m) |

**Returns:** `float` — Capillary pressure $p_c$ (Pa)

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
