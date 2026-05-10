# TheoryOfAlgorithm

Theory of Algorithms lab — 2D cellular automaton with von Neumann neighborhood, implemented in Python with Matplotlib animation and a full LaTeX report.

**Variant 39.** Transition function encoded as the number `59350005`.

## Task

Implement a 2D binary cellular automaton where:
- neighborhood is von Neumann radius-1 (5 cells: center + 4 orthogonal neighbors)
- boundary conditions are **toroidal** (wrap-around, no edge effects)
- transition rules are derived from the variant number
- user selects field size, iteration count, initial pattern, and display mode

## Mathematical Model

The automaton is defined as `CA = (L, S, N, f)`:

| Symbol | Meaning |
|--------|---------|
| `L` | 2D integer lattice `[0, W-1] × [0, H-1]` |
| `S` | Binary states `{0, 1}` |
| `N(i,j)` | `{(i,j), (i-1,j), (i+1,j), (i,j-1), (i,j+1)}` |
| `f` | Local transition function |

Evolution equation: `s(t+1, x) = f(N(s(t, x)))`

### Neighborhood state encoding

Each cell's 5-cell neighborhood is encoded as a 5-bit integer (0–31):

```
state = center×16 + top×8 + right×4 + bottom×2 + left×1
```

### Transition rules

`n = 11 × variant × day × month × year = 59350005`

`59350005` in binary, zero-padded to 32 bits: `00000011100010100110010010110101`. Each bit `i` gives the output for neighborhood state `i`. Out of 32 rules: **13 map to 1** (40.6%), **19 map to 0** (59.4%).

### Toroidal boundary conditions

```python
neighbors[(y - 1) % height, x]   # top
neighbors[y, (x + 1) % width]    # right
neighbors[(y + 1) % height, x]   # bottom
neighbors[y, (x - 1) % width]    # left
```

## Implementation

### `NeumannCellularAutomaton` class

| Method | Description |
|--------|-------------|
| `_generate_rules_from_id(n)` | Convert number to 32-entry rule dict |
| `get_neumann_neighbors(x, y)` | Return 4 neighbor states with toroidal wrap |
| `get_neighborhood_state(x, y)` | Compute 5-bit neighborhood code |
| `update()` | One evolution step: apply rules to all cells simultaneously |
| `set_random_initial_state(density)` | `np.random.choice([0,1], p=[1-d, d])` |
| `set_manual_initial_state(pattern)` | Initialize from a named pattern |
| `run_simulation(iterations, visualize)` | Dispatch to console or GUI mode |
| `visualize_simulation(iterations)` | `FuncAnimation` with live cell count graph |
| `analyze_behavior(max_iterations)` | Run headlessly, detect stabilization, plot stats |

### Initial patterns (8 options)

| Choice | Pattern |
|--------|---------|
| 1 | Random (50% density) |
| 2 | Horizontal waves (stripes every 2 rows) |
| 3 | Checkerboard (2×2 cells) |
| 4 | Spiral (parametric, radius + random scatter) |
| 5 | Dot grid (spacing = 5) |
| 6 | Single cross (center pixel + 4 neighbors) |
| 7 | Random dense (70%) |
| 8 | Random sparse (30%) |

### Display modes

- **Console** — text grid + per-step statistics table (step / live cells / density)
- **Graphical** — Matplotlib `FuncAnimation`: left panel shows the grid, right panel shows live-cell count over time

### Behavior analysis

`analyze_behavior()` runs the automaton headlessly, records `live_cells` and `density` per step, stops early on stabilization (`live_history[-1] == live_history[-2]`), then plots 4 charts: live cell dynamics, density dynamics, histogram, and rate of change.

## Wolfram Classification

The automaton (rule number 59350005) exhibits **Class IV** behavior:
- Density stabilizes at ~43% regardless of field size or initial conditions
- Local changes in initial state do not predictably affect long-term evolution
- System sustains patterns but no stable oscillators or gliders emerge

Pattern-specific outcomes:
- **Cross** → reaches static state after 274 iterations
- **Dot grid** → pattern is preserved but shifts downward dynamically
- **Checkerboard** → cycles through 12 repeating patterns indefinitely
- **Spiral / random** → expands with structure, then collapses into chaos

## Dependencies

```
numpy
matplotlib
```

## Run

```bash
cd theory_of_algorithm
python main.py
```
