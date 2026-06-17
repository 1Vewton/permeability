# permeability

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/1Vewton/permeability)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/permeability?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/permeability)

[中文](README.zh_CN.md)
[English](README.md)

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

### Anisotropic Permeability Tensor

For **orthotropic media** (e.g., woven composites), the permeability is represented as a diagonal tensor:

$$
K = \begin{bmatrix}
K_x & 0 & 0 \\
0 & K_y & 0 \\
0 & 0 & K_z
\end{bmatrix}
$$

The **Darcy velocity** in anisotropic media is:

$$
v = -\frac{1}{\mu} \cdot K \cdot \nabla p
$$

After coordinate rotation, the tensor transforms as:

$$
K' = R \cdot K \cdot R^T
$$

The **effective permeability** in an arbitrary direction (unit vector $n$) is:

$$
K_{\text{eff}} = n^T \cdot K \cdot n
$$

Key derived quantities include the **in-plane average**, **anisotropy ratio**, and **degree of anisotropy**:

$$
K_{\text{in-plane}} = \frac{K_x + K_y}{2}, \qquad
\beta = \frac{K_{\text{in-plane}}}{K_z}, \qquad
\delta = 1 - \frac{\min(K_x, K_y, K_z)}{\max(K_x, K_y, K_z)}
$$

For a full symmetric tensor $K$ (with off-diagonal components), the **principal permeability values** are its eigenvalues $K_1 \ge K_2 \ge K_3$, and the **principal directions** are the corresponding eigenvectors, obtained via eigenvalue decomposition:

$$
K \cdot \phi_i = K_i \cdot \phi_i
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

### Anisotropic Permeability Tensor

For orthotropic materials (e.g., woven composites), the `PermeabilityTensor` class represents a diagonal permeability tensor $K = \text{diag}(K_x, K_y, K_z)$.

```python
from permeability.permeability.AnisotropicTensor import PermeabilityTensor

# Construct from principal values (orthotropic)
tensor = PermeabilityTensor.from_principal_values(

    Kx=1e-12,  # Warp/fiber direction (m²)
    Ky=5e-13,  # Weft direction (m²)
    Kz=1e-13   # Through-thickness direction (m²)
)

# Isotropic tensor
iso_tensor = PermeabilityTensor.from_isotopic(K=1e-12)

# Transversely isotropic (e.g., unidirectional fiber bundles)
trans_tensor = PermeabilityTensor.from_transversely_isotropic(
    K_in_plane=1e-12,
    K_out_plane=1e-13
)
```

**Tensor Properties**

```python
# 3x3 diagonal matrix
print(tensor.tensor)

# Average in-plane permeability (Kx + Ky) / 2
print(f"In-plane avg: {tensor.in_plane_average:.3e} m²")

# Anisotropy ratio β = in_plane_avg / Kz
print(f"Anisotropy ratio: {tensor.anisotropy_ratio:.2f}")

# Degree of anisotropy (0 = isotropic, 1 = fully anisotropic)
print(f"Degree of anisotropy: {tensor.degree_of_anisotropy:.3f}")

# Export to dictionary
print(tensor.to_dict())
```

**Darcy Velocity in Anisotropic Media**

```python
import numpy as np

# Darcy velocity: v = -(1/μ) · K · ∇p
grad_p = np.array([1000, 500, 100])  # Pressure gradient (Pa/m)
v = tensor.darcy_velocity(grad_p=grad_p, mu=0.192)
print(f"Darcy velocity: {v} m/s")
```

**Effective Permeability in a Direction**

```python
# Along principal axes
print(tensor.effective_permeability_in_direction(direction='x'))
print(tensor.effective_permeability_in_direction(direction='xy'))  # in-plane avg

# In an arbitrary direction
n = np.array([1, 1, 0])  # arbitrary direction vector
print(tensor.effective_permeability_in_direction(direction_vector=n))
```

### Anisotropic Darcy Flux

The `anisotropic_darcy_flux` function computes Darcy flux and related quantities in anisotropic media.

```python
from permeability.permeability.AnisotropicTensor import (
    PermeabilityTensor,
    anisotropic_darcy_flux
)

tensor = PermeabilityTensor.from_principal_values(
    Kx=1e-12, Ky=5e-13, Kz=1e-13
)

result = anisotropic_darcy_flux(
    tensor=tensor,
    grad_p=np.array([1000, 500, 100]),  # Pa/m
    mu=0.192,                            # Pa·s
    area_normal=np.array([1, 0, 0])      # Optional: unit normal of cross-section
)
print(f"Darcy velocity: {result['darcy_velocity']} m/s")
print(f"Flux magnitude: {result['flux_magnitude']:.3e} m/s")
print(f"Velocity angle from gradP: {result['velocity_angle_from_gradP_deg']:.2f}°")
print(f"Area flux: {result['area_flux']:.3e} m³/s per m²")
```

### Anisotropy Evolution Across PIP Cycles

The `anisotropy_evolution` function analyzes how permeability anisotropy evolves over multiple **PIP (Polymer Infiltration and Pyrolysis) cycles**, which is critical for understanding the densification process of ceramic matrix composites (CMCs).

$$
K_i = \begin{bmatrix}
K_{x,i} & 0 & 0 \\
0 & K_{y,i} & 0 \\
0 & 0 & K_{z,i}
\end{bmatrix}
,\qquad
\beta_i = \frac{K_{\text{in-plane},i}}{K_{z,i}}
,\qquad
\delta_i = 1 - \frac{\min(K_{x,i}, K_{y,i}, K_{z,i})}{\max(K_{x,i}, K_{y,i}, K_{z,i})}
$$

$$
\text{Anisotropy Reduction} = \frac{\beta_0 - \beta_n}{\beta_0} \times 100\%
$$

```python
from permeability.permeability.AnisotropicTensor import anisotropy_evolution
import numpy as np

# Permeability data across PIP cycles: each row = [Kx, Ky, Kz]
K_data = np.array([
    [1.0e-12, 5.0e-13, 1.0e-13],   # Cycle 0 (as-processed)
    [8.0e-13, 4.5e-13, 1.5e-13],   # Cycle 1
    [6.0e-13, 4.0e-13, 2.0e-13],   # Cycle 2
    [4.5e-13, 3.5e-13, 2.5e-13],   # Cycle 3
])
cycles = np.array([0, 1, 2, 3])

result = anisotropy_evolution(K_values=K_data, cycles=cycles)

# Access results
for i, cycle in enumerate(result['cycles']):
    print(f"Cycle {cycle}: β = {result['anisotropy_ratios'][i]:.2f}, "
          f"δ = {result['degrees_of_anisotropy'][i]:.3f}")

print(f"Anisotropy reduction: {result['anisotropy_reduction']:.1f}%")
```

---

## MCP Server

The package includes a **Model Context Protocol (MCP) server** that exposes permeability calculations as AI-accessible tools. After [installing the package](#installation), start the server with:

### Starting the Server

Once installed, simply run:

```bash
# Default port 8000 (HTTP/SSE transport)
permeability_mcp

# Custom port
permeability_mcp --port 8080
```

The server starts via HTTP/SSE transport (`http://localhost:8000` by default).

If you prefer to try it without installing, you can also use:

```bash
uvx --from permeability permeability_mcp
```

### Streamable HTTP Transport

For clients that support the modern **Streamable HTTP** transport (MCP spec), the server can be configured to use HTTP POST-based communication instead of SSE:

```bash
permeability_mcp --port 8000
# Then connect via Streamable HTTP at http://localhost:8000/mcp
```

**Claude Desktop** configuration using Streamable HTTP (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "permeability": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**Cline (VS Code extension)** configuration using Streamable HTTP:

```json
{
  "mcpServers": {
    "permeability": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

> **Note:** The Streamable HTTP transport requires a client that supports the MCP Streamable HTTP specification. The server runs the same underlying implementation — only the transport protocol differs from the default SSE-based connection.

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
| `darcy_m2_converter` | Convert Darcy to m² and/or m² to Darcy (bidirectional) |
| `calculate_darcy_flux_tool` | Compute Darcy flux in anisotropic media; accepts permeability tensor from principal values, isotropic, or transversely isotropic |
| `calculate_anisotropy_evolution_tool` | Analyze anisotropy evolution across PIP cycles; returns tensors, anisotropy ratios, and cycle-by-cycle data |

Each tool accepts the same parameters as the Python API.



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

### `PermeabilityTensor(Kx, Ky, Kz)`

Anisotropic permeability tensor for 2D woven composites. Represents a diagonal permeability tensor $K = \text{diag}(K_x, K_y, K_z)$.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Kx` | float | Permeability in x-direction (warp/fiber direction) (m²) |
| `Ky` | float | Permeability in y-direction (weft direction) (m²) |
| `Kz` | float | Permeability in z-direction (through-thickness) (m²) |

#### Class Methods

**`PermeabilityTensor.from_principal_values(Kx, Ky, Kz)`**

Construct tensor from principal direction permeabilities (orthotropic materials).

**`PermeabilityTensor.from_isotopic(K)`**

Construct an isotropic permeability tensor where $K_x = K_y = K_z = K$.

**`PermeabilityTensor.from_transversely_isotropic(K_in_plane, K_out_plane)`**

Construct a transversely isotropic permeability tensor where $K_x = K_y = K_\text{in-plane}$, $K_z = K_\text{out-plane}$ (suitable for unidirectional fiber bundles).

#### Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `tensor` | `numpy.ndarray` | Full 3x3 diagonal tensor matrix |
| `in_plane_average` | `float` | Average in-plane permeability $(K_x + K_y)\,/\,2$ (m²) |
| `anisotropy_ratio` | `float` | Anisotropy ratio $\beta = \text{in\_plane\_avg}\,/\,K_z$ |
| `degree_of_anisotropy` | `float` | Degree of anisotropy (0 = isotropic, 1 = fully anisotropic) |

#### Methods

**`darcy_velocity(grad_p, mu)`**

Calculate Darcy velocity vector $v = -(1/\mu) \cdot K \cdot \nabla p$.

| Parameter | Type | Description |
|-----------|------|-------------|
| `grad_p` | numpy.ndarray | Pressure gradient vector (Pa/m), shape (3,) |
| `mu` | float | Dynamic viscosity (Pa·s) |

**Returns:** `numpy.ndarray` — Darcy velocity vector (m/s), shape (3,)

**`effective_permeability_in_direction(direction=None, direction_vector=None)`**

Calculate effective permeability in a specified direction. For a direction unit vector $n$, $K_\text{eff} = n^T \cdot K \cdot n$.

| Parameter | Type | Description |
|-----------|------|-------------|
| `direction` | str, optional | One of `'x'`, `'y'`, `'z'`, `'xy'` (in-plane), or `'avg'` |
| `direction_vector` | numpy.ndarray, optional | Arbitrary unit vector of shape (3,) |

**Returns:** `float` — Effective permeability in the specified direction (m²)

**`rotate(R)`**

Rotate the permeability tensor by rotation matrix $R$: $K' = R \cdot K \cdot R^T$.

| Parameter | Type | Description |
|-----------|------|-------------|
| `R` | numpy.ndarray | Orthogonal rotation matrix (3x3) |

**Returns:** `PermeabilityTensor` or `FullTensor` — Rotated tensor (diagonal if off-diagonal terms negligible)

**`to_dict()`**

Export tensor data as a dictionary with keys: `Kx`, `Ky`, `Kz`, `in_plane_average`, `anisotropy_ratio`, `degree_of_anisotropy`.

**Returns:** `dict`

---

### `FullTensor(matrix)`

Full 3x3 symmetric permeability tensor with off-diagonal components, used after coordinate rotation.

| Parameter | Type | Description |
|-----------|------|-------------|
| `matrix` | numpy.ndarray | Full 3x3 symmetric tensor matrix |

#### Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `principal_values` | `tuple` | Principal permeability values $(K_1, K_2, K_3)$, descending order |
| `principal_directions` | `numpy.ndarray` | Principal permeability directions (eigenvectors), shape (3, 3) |

#### Methods

**`to_principal_tensor()`**

Convert to diagonal `PermeabilityTensor` in the principal coordinate system using eigenvalues.

**Returns:** `PermeabilityTensor`

---

### `anisotropic_darcy_flux(tensor, grad_p, mu, area_normal=None)`

Compute Darcy flux and related quantities for anisotropic media.

| Parameter | Type | Description |
|-----------|------|-------------|
| `tensor` | PermeabilityTensor | Anisotropic permeability tensor |
| `grad_p` | numpy.ndarray | Pressure gradient vector (Pa/m) |
| `mu` | float | Dynamic viscosity (Pa·s) |
| `area_normal` | numpy.ndarray, optional | Unit normal vector of cross-section area for flux computation |

**Returns:** `dict` with keys:
| Key | Description |
|-----|-------------|
| `darcy_velocity` | Darcy velocity vector (m/s) |
| `flux_magnitude` | Magnitude of Darcy velocity (m/s) |
| `velocity_angle_from_gradP_deg` | Angle between velocity and pressure gradient (degrees) |
| `area_flux` | Volumetric flux per unit area (m³/s per m²), only if `area_normal` provided |

---

### `anisotropy_evolution(K_values, cycles)`

Analyze the evolution of permeability anisotropy across PIP (Polymer Infiltration and Pyrolysis) cycles.

| Parameter | Type | Description |
|-----------|------|-------------|
| `K_values` | numpy.ndarray | 2D array where each row is $[K_x, K_y, K_z]$ for one PIP cycle, shape (n, 3) |
| `cycles` | numpy.ndarray | 1D array of PIP cycle numbers, shape (n,) |

**Returns:** `dict` with keys:
| Key | Description |
|-----|-------------|
| `tensors` | List of `PermeabilityTensor` objects for each cycle |
| `cycles` | Array of cycle numbers |
| `anisotropy_ratios` | Array of anisotropy ratios $\beta$ for each cycle |
| `degrees_of_anisotropy` | Array of degree of anisotropy $\delta$ for each cycle |
| `anisotropy_reduction` | Percentage reduction in anisotropy from first to last cycle (%) |

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
