# Error Propagation Rocket

![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

My Computational Lab Assignment about error propagation: a formula that **calculates** π (Leibniz series), with baselines 3.1415 and 3.1416 (truncate vs round to 4 decimals), showing the 20th, 40th, 60th, and 100th term and the gap between the two baselines.

## What It Demonstrates

This project follows the assignment requirements:

- **A formula that uses/calculates π** — We use the **Leibniz/Gregory series** to compute π: $\frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots$
- **Baselines 3.1416 and 3.1415** — These are the **starting approximations**: one is π truncated to 4 decimal places (3.1415), the other rounded to 4 decimals (3.1416). At each step we compare these two ways of approximating.
- **20th, 40th, 60th, 100th** — We report the value of π at the **20th, 40th, 60th, and 100th term** of the Leibniz series for both baselines (truncate to 4 dec vs round to 4 dec).
- **The gap** — At each of those terms we show the **difference** between the truncated and rounded baseline so you can see how the small difference propagates.
- **Present using Python** — Table plus **rocket visualization**: two rockets driven by π from Leibniz at each step (trunc vs round baseline).

## Visual Preview

### Console output

Running `python error_propagation_rocket.py --table-only` prints the comparison table. The exact numbers and an explanation of when the gap is 0 vs 0.0001 are in the [Results](#results) section below.

![Console output: Error Propagation table](assets/console.png?v=2)

### Rocket visualization (step-by-step)

**Term 20**

![Term 20](assets/20.png?v=2)

**Term 40**

![Term 40](assets/40.png?v=2)

**Term 60**

![Term 60](assets/60.png?v=2)

**Term 100**

![Term 100](assets/100.png?v=2)

**Animated**

![Rocket animation](assets/rocket.gif?v=2)

## Requirements

- **Python** 3.7 or higher
- **turtle** (included in the Python standard library; only needed for `--viz`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RodneeGlenMartin/Martin_lab_assignment_1_computational_science.git
   cd Martin_lab_assignment_1_computational_science
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

3. (Optional) Install dependencies if you add any later:
   ```bash
   pip install -r requirements.txt
   ```
   The script runs with the standard library only (turtle is built-in).

## Usage

**Default (table then visualization):**
```bash
python error_propagation_rocket.py
```

**Options:**

| Flag | Description |
|------|-------------|
| `--table-only` | Print the comparison table and exit (no visualization). |
| `--viz`        | Show only the rocket visualization (no console table). |
| `--steps 20 40 60 100` | Which terms to report (default: 20 40 60 100). |

Examples:
```bash
python error_propagation_rocket.py --table-only
python error_propagation_rocket.py --viz
python error_propagation_rocket.py --steps 10 50 100
```

## Results

Running the script produces the following table at the **20th, 40th, 60th, and 100th term** of the Leibniz series:

| Term | Partial π | Trunc (4 dec) | Round (4 dec) | Gap |
|------|-----------|---------------|---------------|-----|
| 20   | 3.091623806667840 | 3.0916 | 3.0916 | 0.000000000000000 |
| 40   | 3.116596556793833 | 3.1165 | 3.1166 | 0.000100000000000 |
| 60   | 3.124927143928997 | 3.1249 | 3.1249 | 0.000000000000000 |
| 100  | 3.131592903558554 | 3.1315 | 3.1316 | 0.000100000000000 |

**Why is the gap zero at term 20 and 60 but not at 40 and 100?**  
The **gap** is the difference between “round to 4 decimals” and “truncate to 4 decimals”. That difference is 0 when the **5th decimal digit** of the partial π is 0–4 (rounding does not change the 4th decimal), and it is **0.0001** when the 5th digit is 5–9 (rounding bumps the 4th decimal up by one). So:

- **Term 20:** partial π = 3.091**6**23806… → 5th decimal is **2** → trunc and round both give 3.0916 → **Gap = 0**.
- **Term 40:** partial π = 3.116**5**96556… → 5th decimal is **9** → trunc 3.1165, round 3.1166 → **Gap = 0.0001**.
- **Term 60:** partial π = 3.124**9**27143… → 5th decimal is **2** → both give 3.1249 → **Gap = 0**.
- **Term 100:** partial π = 3.131**5**92903… → 5th decimal is **9** → trunc 3.1315, round 3.1316 → **Gap = 0.0001**.

So the Leibniz results are correct: the gap appears only when rounding to 4 decimals changes the value relative to truncation.

---

## Mathematical Explanation

**Formula that calculates π (Leibniz/Gregory series):**

$$
\frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \cdots
$$

So $\pi = 4 \sum_{k=0}^{n-1} \frac{(-1)^k}{2k+1}$ after $n$ terms.

**Baselines:** At each term we take the partial sum and form two 4-decimal approximations:

- **Truncate to 4 decimals:** keep only the first four decimals (e.g. 3.14159265… → 3.1415).
- **Round to 4 decimals:** round at the fourth decimal (e.g. 3.14159265… → 3.1416 when the 5th digit ≥ 5).

**Reported terms:** The table and the rocket visualization both report the **20th, 40th, 60th, and 100th term**: partial π, trunc (4 dec), round (4 dec), and the **gap** (absolute difference between the two baselines) at each of those terms.

## Features

- **Formula that calculates π** — Leibniz/Gregory series (no external π; we compute it).
- **Baselines 3.1415 and 3.1416** — Truncate vs round to 4 decimals at each step.
- **20th, 40th, 60th, 100th term** — Table reports partial π, trunc (4 dec), round (4 dec), and the gap at each of these terms.
- **Console table** — Columns: Term, Partial π, Trunc (4 dec), Round (4 dec), Gap.
- **Rocket visualization (Leibniz-connected)** — Two rockets trace trajectories using π from the Leibniz series at each step: green = truncated to 4 dec, cyan = rounded to 4 dec. The vector magnitude and gap are shown at terms 20, 40, 60, 100. Run with `--viz` for rockets only, or run with no flags for table then rockets.

## Educational Context

Suitable for:

- Computational or numerical methods labs
- Demonstrating **error propagation** and sensitivity to input precision
- Discussing **rounding vs truncation** (e.g. 3.1415 vs 3.1416)
- Visualizing small numerical differences in a memorable way

## Acknowledgments

This project was completed as part of a **computational lab assignment** to demonstrate error propagation and numerical sensitivity in vector calculations.

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

