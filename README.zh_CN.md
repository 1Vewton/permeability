# permeability

一个基于 **渗流距离法** 计算多孔介质渗透率的 Python 包，源自达西定律公式，并通过 Young-Laplace 方程进行 **毛细管压力修正**：

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

### 毛细管修正形式

当考虑毛细管压力 $p_c$ 时，$\Delta P$ 替换为 $(\Delta P + p_c)$：

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

| 符号 | 含义 | 单位 |
|--------|---------|------|
| $K$ | 渗透率 | m² |
| $L$ | 沿流动方向的样品厚度 | m |
| $\mu$ | 流体的动力粘度 | Pa·s |
| $\phi$ | 多孔介质的孔隙率 | 无量纲 |
| $t$ | 流体完全渗透样品的时间 | s |
| $\Delta P$ | 样品两端的恒定压差 | Pa |
| $z$ | 渗流前锋位置 | m |
| $p_c$ | 毛细管压力 | Pa |
| $\gamma$ | 液体表面张力 | N/m |
| $\theta$ | 接触角（润湿角） | 度 |
| $r$ | 等效孔隙半径 | m |

本包还提供了 **MCP 服务器**，可将这些计算以工具形式暴露给 AI 助手（如 Claude）。

---

## 安装

### 使用 pip

```bash
pip install permeability
```

### 使用 uv（推荐）

```bash
uv add permeability
```

---

## 快速入门

### 根据实验数据计算渗透率

```python
from permeability.permeability import Seepage

# 实验参数
K = Seepage.calculate_permeability(
    L=0.003,   # 样品厚度: 3 mm
    mu=0.192,  # 流体粘度: 0.192 Pa·s
    phi=0.445, # 孔隙率: 0.445
    t=100,     # 渗透时间: 100 s
    dP=1e4     # 压差: 10,000 Pa
)
print(f"渗透率: {K:.3e} m²")  # ~3.84e-13 m²
```

### 预测渗透时间

```python
t = Seepage.calculate_infiltration_time(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    dP=1e4
)
print(f"渗透时间: {t:.2f} s")  # ~100.00 s
```

### 计算渗流前锋位置

```python
# 单时间点
z = Seepage.calculate_infiltration_front_position(
    K=1.284e-13,
    mu=0.192,
    phi=0.642,
    dP=1e5,
    t=120
)
print(f"前锋位置: {z:.4f} m")  # ~0.0050 m

# 多个时间点（用于绘图）
import numpy as np
z_array = Seepage.calculate_infiltration_front_position_with_multiple_time(
    K=1.284e-13,
    mu=0.192,
    phi=0.642,
    dP=1e5,
    t=np.array([0, 30, 120])
)
print(f"前锋位置数组: {z_array}")  # [0.0, 0.0025, 0.005]
```

### 计算毛细管压力

```python
from permeability.permeability.Capillary import calculate_capillary_pressure

# 通过 Young-Laplace 方程计算毛细管压力
p_c = calculate_capillary_pressure(
    gamma=0.072,  # 水的表面张力: 0.072 N/m
    theta=30,     # 接触角: 30 度
    r=1e-6        # 孔隙半径: 1 µm
)
print(f"毛细管压力: {p_c:.2f} Pa")  # ~124.71 Pa
```

### 考虑毛细管修正的渗透率计算

```python
# 考虑毛细管压力计算渗透率
K_corrected = Seepage.calculate_permeability(
    L=0.003,
    mu=0.192,
    phi=0.445,
    t=100,
    dP=1e4,
    p_c=124.71  # 毛细管压力 (Pa)
)
print(f"修正后渗透率: {K_corrected:.3e} m²")
```

### 计算压差

```python
# 计算样品两端的压差
dP = Seepage.calculate_pressure_difference(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    t=100
)
print(f"压差: {dP:.2f} Pa")  # ~10000.00 Pa

# 考虑毛细管修正
dP_corrected = Seepage.calculate_pressure_difference(
    L=0.003,
    mu=0.192,
    phi=0.445,
    K=3.8448e-13,
    t=100,
    p_c=124.71  # 毛细管压力 (Pa)
)
print(f"修正后压差: {dP_corrected:.2f} Pa")
```

### 单位转换

```python
from permeability.utils.UnitConverter import darcy2m2, m22darcy

# 将 m² 转换为 Darcy
darcy = m22darcy(m2K=3.8448e-13)
print(f"渗透率: {darcy:.3f} Darcy")  # ~0.390 Darcy

# 将 Darcy 转换为 m²
m2 = darcy2m2(darcyK=0.3896)
print(f"渗透率: {m2:.3e} m²")  # ~3.845e-13 m²
```

---

## MCP 服务器

本包包含一个 **模型上下文协议 (MCP) 服务器**，可将渗透率计算以工具形式提供给 AI 助手使用。[安装本包](#安装)后，通过以下方式启动服务器：

### 启动服务器

安装后，直接运行：

```bash
# 默认端口 8000
permeability_mcp

# 自定义端口
permeability_mcp --port 8080
```

服务器通过 HTTP/SSE 传输启动（默认为 `http://localhost:8000`）。

如果不想安装，也可以尝试：

```bash
uvx --from permeability permeability_mcp
```

### AI 助手配置

#### 对于 **Claude Desktop**，添加到 `claude_desktop_config.json`：

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

#### 对于 **Cline（VS Code 扩展）**，添加到 MCP 设置：

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

### 可用工具

MCP 服务器运行后，AI 助手可以调用以下工具：

| 工具 | 描述 |
|------|-------------|
| `calculate_permeability_by_seepage_distance` | 计算 $K$（可通过 $p_c$ 进行毛细管修正） |
| `calculate_infiltration_time` | 计算 $t$（可通过 $p_c$ 进行毛细管修正） |
| `calculate_infiltration_front_position` | 计算 $z(t)$（可通过 $p_c$ 进行毛细管修正） |
| `calculate_infiltration_front_position4multiple_times` | 计算多个时间点的 $z(t)$（可通过 $p_c$ 进行毛细管修正） |
| `calculate_capillary_pressure` | 计算 $p_c = 2\gamma\cos(\theta)\,/\,r$（Young-Laplace 方程） |
| `calculate_pressure_difference` | 计算 $\Delta P$（可通过 $p_c$ 进行毛细管修正） |
| `darcy_to_m2_converter` | 将 Darcy 转换为 m² |
| `m2_to_darcy_converter` | 将 m² 转换为 Darcy |

每个工具接受与 Python API 相同的参数。

---

## API 参考

### `Seepage.calculate_permeability(L, mu, phi, t, dP, p_c=None)`

根据渗流距离实验数据计算渗透率。提供 $p_c$ 时使用毛细管修正形式。

$$
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot \Delta P}
\qquad\text{或}\qquad
K = \frac{L^2 \cdot \mu \cdot \phi}{2 \cdot t \cdot (\Delta P + p_c)}
$$

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `L` | float | 沿流动方向的样品长度/厚度 (m) |
| `mu` | float | 流体的动力粘度 (Pa·s) |
| `phi` | float | 多孔介质的孔隙率 ($0 < \phi \le 1$) |
| `t` | float | 流体完全渗透样品的总时间 (s) |
| `dP` | float | 样品两端的恒定压差 (Pa) |
| `p_c` | float, 可选 | 用于修正的毛细管压力 (Pa) |

**返回：** `float` — 渗透率 $K$ (m²)

---

### `Seepage.calculate_infiltration_time(L, mu, phi, K, dP, p_c=None)`

预测流体完全渗透样品所需的时间。提供 $p_c$ 时使用毛细管修正形式。

$$
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot \Delta P}
\qquad\text{或}\qquad
t = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot (\Delta P + p_c)}
$$

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `L` | float | 沿流动方向的样品长度/厚度 (m) |
| `mu` | float | 流体的动力粘度 (Pa·s) |
| `phi` | float | 多孔介质的孔隙率 ($0 < \phi \le 1$) |
| `K` | float | 渗透率 (m²) |
| `dP` | float | 样品两端的恒定压差 (Pa) |
| `p_c` | float, 可选 | 用于修正的毛细管压力 (Pa) |

**返回：** `float` — 渗透时间 $t$ (s)

---

### `Seepage.calculate_infiltration_front_position(K, mu, phi, dP, t, p_c=None)`

计算给定时间的渗流前锋位置。提供 $p_c$ 时使用毛细管修正形式。

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
\qquad\text{或}\qquad
z(t) = \sqrt{\frac{2 \cdot K \cdot (\Delta P + p_c) \cdot t}{\mu \cdot \phi}}
$$

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `K` | float | 渗透率 (m²) |
| `mu` | float | 流体的动力粘度 (Pa·s) |
| `phi` | float | 多孔介质的孔隙率 ($0 < \phi \le 1$) |
| `dP` | float | 样品两端的恒定压差 (Pa) |
| `t` | float | 经过的时间 (s) |
| `p_c` | float, 可选 | 用于修正的毛细管压力 (Pa) |

**返回：** `float` — 渗流前锋位置 $z$ (m)

---

### `Seepage.calculate_infiltration_front_position_with_multiple_time(K, mu, phi, dP, t, p_c=None)`

计算多个时间点的渗流前锋位置（适用于绘图）。提供 $p_c$ 时使用毛细管修正形式。

$$
z(t) = \sqrt{\frac{2 \cdot K \cdot \Delta P \cdot t}{\mu \cdot \phi}}
\qquad\text{或}\qquad
z(t) = \sqrt{\frac{2 \cdot K \cdot (\Delta P + p_c) \cdot t}{\mu \cdot \phi}}
$$

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `K` | float | 渗透率 (m²) |
| `mu` | float | 流体的动力粘度 (Pa·s) |
| `phi` | float | 多孔介质的孔隙率 ($0 < \phi \le 1$) |
| `dP` | float | 样品两端的恒定压差 (Pa) |
| `t` | numpy.ndarray | 时间值数组 (s) |
| `p_c` | float, 可选 | 用于修正的毛细管压力 (Pa) |

**返回：** `numpy.ndarray` — 渗流前锋位置数组 $z$ (m)

---

### `Seepage.calculate_pressure_difference(L, mu, phi, K, t, p_c=None)`

计算样品两端的压差。提供 $p_c$ 时使用毛细管修正形式。

$$
\Delta P = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot t}
\qquad\text{或}\qquad
\Delta P = \frac{\mu \cdot \phi \cdot L^2}{2 \cdot K \cdot t} - p_c
$$

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `L` | float | 沿流动方向的样品长度/厚度 (m) |
| `mu` | float | 流体的动力粘度 (Pa·s) |
| `phi` | float | 多孔介质的孔隙率 ($0 < \phi \le 1$) |
| `K` | float | 渗透率 (m²) |
| `t` | float | 流体完全渗透样品的总时间 (s) |
| `p_c` | float, 可选 | 用于修正的毛细管压力 (Pa) |

**返回：** `float` — 压差 $\Delta P$ (Pa)

---

### `calculate_capillary_pressure(gamma, theta, r)`

使用 **Young-Laplace 方程** 计算毛细管压力。

$$
p_c = \frac{2 \cdot \gamma \cdot \cos(\theta)}{r}
$$

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `gamma` | float | 液体的表面张力 (N/m) |
| `theta` | float | 接触角 / 润湿角 (度) |
| `r` | float | 等效孔隙半径 (m) |

**返回：** `float` — 毛细管压力 $p_c$ (Pa)

---

### `darcy2m2(darcyK)`

将渗透率从 Darcy 转换为 m²。

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `darcyK` | float | 以 Darcy 为单位的渗透率 |

**返回：** `float` — 以 m² 为单位的渗透率

---

### `m22darcy(m2K)`

将渗透率从 m² 转换为 Darcy。

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `m2K` | float | 以 m² 为单位的渗透率 |

**返回：** `float` — 以 Darcy 为单位的渗透率

---

## 开发

### 设置

```bash
git clone https://github.com/1Vewton/permeability.git
cd permeability
uv sync
```

### 运行测试

```bash
uv run pytest
```

### 代码风格

```bash
uv run flake8
```

---

## 许可证

本项目基于 **GNU General Public License v3.0** 许可。详情请参阅 [LICENSE](LICENSE) 文件。
