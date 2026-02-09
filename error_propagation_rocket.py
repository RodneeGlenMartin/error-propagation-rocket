"""
Error Propagation Rocket — visualization of how a small difference in π (3.1415 vs 3.1416)
propagates through the vector magnitude formula sqrt((π·step)² + step²).

Run with Python to see a console comparison table and a turtle animation of the two
trajectories. Use --table-only or --viz-only to run only one part; use --steps to
customize which steps are highlighted.
"""

import argparse
from typing import List, Optional
import time
import turtle
import mpmath

# ---------------------------------------------------------------------------
# High-precision and π baselines
# ---------------------------------------------------------------------------
mpmath.mp.dps = 50
PI_HI = mpmath.pi
# Baselines per instructions: 3.1416 and 3.1415 (used in formula for comparison)
PI_BASELINE_1 = mpmath.mpf("3.1416")
PI_BASELINE_2 = mpmath.mpf("3.1415")
# For display: baseline_2 is truncation of π at 4 decimals, baseline_1 is rounded
PI_TRUNC = PI_BASELINE_2
PI_ROUND = PI_BASELINE_1

# Steps highlighted in table and animation (can be overridden via --steps)
STEPS = [20, 40, 60, 100]
# Table: steps 1..MAX_STEP printed; only those in STEPS are shown per row
MAX_STEP = 100
# Angle in visualization: angle = π * step / ANGLE_DIVISOR (radians)
ANGLE_DIVISOR = 50.0

# Turtle visualization tuning
SCALE = 3.5
VISUAL_AMPLIFICATION = 500
STEP_DELAY = 0.05
STOP_AT_STEP_SEC = 0.8


def calculate_quadrature_vector(pi_value: mpmath.mpf, step: int) -> mpmath.mpf:
    """
    Rocket diagonal vector magnitude: sqrt((pi*step)² + step²).

    Represents the Euclidean length of the vector (π·step, step). Used to compare
    how truncated vs rounded π affect the result as step increases.

    Args:
        pi_value: Value of π (e.g. PI_TRUNC or PI_ROUND).
        step: Step index (positive integer).

    Returns:
        Magnitude as an mpmath float.

    Raises:
        ValueError: If step is not positive.
    """
    if step <= 0:
        raise ValueError(f"step must be positive, got {step}")
    if step > 1_000_000:
        raise ValueError(f"step too large (max 1000000), got {step}")
    return mpmath.sqrt((pi_value * step) ** 2 + step**2)


def print_comparison_table(
    steps_highlight: Optional[List[int]] = None,
    max_step: int = MAX_STEP,
    precision: int = 15,
) -> None:
    """
    Print a comparison table of vector magnitudes for truncated vs rounded π.

    Only rows for steps in steps_highlight are printed; the Gap column shows
    |Vec Round − Vec Trunc|. Default highlights steps 20, 40, 60, 100.
    """
    steps = steps_highlight if steps_highlight is not None else STEPS
    col_step = "Step"
    col_trunc = "Vec Trunc"
    col_round = "Vec Round"
    col_gap = "The Gap"
    width_step = 6
    width_val = max(28, precision + 10)
    width_gap = max(28, precision + 10)

    print("\n--- Error Propagation: Rocket Vector Quadrature (Truncated vs Rounded Pi, mpmath) ---")
    print("(The Gap shows how the small Pi difference propagates in vector magnitude over larger steps.)\n")

    header = f"{col_step:<{width_step}} | {col_trunc:<{width_val}} | {col_round:<{width_val}} | {col_gap:<{width_gap}}"
    separator = "-" * len(header)
    print(header)
    print(separator)

    for step in range(1, max_step + 1):
        if step in steps:
            val_trunc = calculate_quadrature_vector(PI_TRUNC, step)
            val_round = calculate_quadrature_vector(PI_ROUND, step)
            gap = abs(val_round - val_trunc)
            print(
                f"{step:<{width_step}} | {float(val_trunc):<{width_val}.{precision}f} | "
                f"{float(val_round):<{width_val}.{precision}f} | {float(gap):<{width_gap}.{precision}f}"
            )

    print(separator)
    print()


def run_turtle_visualization(
    steps_highlight: Optional[List[int]] = None,
    max_step: int = MAX_STEP,
) -> None:
    """
    Run the turtle animation: two trajectories (trunc vs round π) with amplified angle difference.

    Green turtle = Vec Trunc (3.1415), cyan = Vec Round (3.1416). At steps in
    steps_highlight, the current vector values and gap are shown on screen.
    """
    steps = steps_highlight if steps_highlight is not None else STEPS
    screen = turtle.Screen()
    screen.setup(900, 700)
    screen.bgcolor("#0a0a0f")
    screen.title("Rocket Vector Quadrature Error")
    screen.setworldcoordinates(-380, -380, 380, 380)
    turtle.tracer(0)

    def position_from_angle(angle_rad: float, s: int) -> tuple:
        radius = s * SCALE
        x = float(radius * mpmath.cos(angle_rad))
        y = float(radius * mpmath.sin(angle_rad))
        return (x, y)

    t1 = turtle.Turtle()
    t1.shape("triangle")
    t1.shapesize(1.0, 1.4)
    t1.setheading(90)
    t1.penup()
    t1.color("#00ff88")
    t1.pensize(2)
    t1.speed(0)

    t2 = turtle.Turtle()
    t2.shape("triangle")
    t2.shapesize(1.0, 1.4)
    t2.setheading(90)
    t2.penup()
    t2.color("#00ccff")
    t2.pensize(2)
    t2.speed(0)

    value_header = turtle.Turtle()
    value_header.hideturtle()
    value_header.penup()
    value_header.color("#cccccc")
    value_header.goto(0, 220)
    value_header.write(
        f"{'Step':>4}   —   {'Vec (3.1415)':>18}   —   {'Vec (3.1416)':>18}   —   {'Gap':>18}",
        align="center",
        font=("Consolas", 14, "bold"),
    )
    value_line = turtle.Turtle()
    value_line.hideturtle()
    value_line.penup()
    value_line.color("#00ff88")
    value_line.goto(0, 190)

    start0 = position_from_angle(0.0, 0)
    t1.goto(start0)
    t2.goto(start0)
    t1.pendown()
    t2.pendown()

    for step in range(1, max_step + 1):
        angle_trunc = float(PI_TRUNC * step / ANGLE_DIVISOR)
        angle_round_true = float(PI_ROUND * step / ANGLE_DIVISOR)
        angle_round_visual = angle_trunc + (angle_round_true - angle_trunc) * VISUAL_AMPLIFICATION

        pos_trunc = position_from_angle(angle_trunc, step)
        pos_round = position_from_angle(angle_round_visual, step)

        t1.goto(pos_trunc)
        t2.goto(pos_round)

        turtle.update()
        time.sleep(STEP_DELAY)

        if step in steps:
            val_trunc = calculate_quadrature_vector(PI_TRUNC, step)
            val_round = calculate_quadrature_vector(PI_ROUND, step)
            gap = abs(val_round - val_trunc)

            value_line.clear()
            value_line.write(
                f"{int(step):>4}   —   {float(val_trunc):>18.10f}   —   {float(val_round):>18.10f}   —   {float(gap):>18.10f}",
                align="center",
                font=("Consolas", 14, "normal"),
            )
            turtle.update()
            time.sleep(STOP_AT_STEP_SEC)

    t1.penup()
    t2.penup()

    label1 = turtle.Turtle()
    label1.hideturtle()
    label1.penup()
    label1.color("#00ff88")
    label1.goto(t1.xcor() - 12, t1.ycor())
    label1.write("Vec Trunc", align="right", font=("Arial", 14, "bold"))
    label2 = turtle.Turtle()
    label2.hideturtle()
    label2.penup()
    label2.color("#00ccff")
    label2.goto(t2.xcor() - 12, t2.ycor())
    label2.write("Vec Round", align="right", font=("Arial", 14, "bold"))

    turtle.tracer(1)
    turtle.exitonclick()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Error Propagation Rocket: compare vector magnitude for π ≈ 3.1415 vs 3.1416.",
    )
    parser.add_argument(
        "--table-only",
        action="store_true",
        help="Print the comparison table and exit (no turtle window).",
    )
    parser.add_argument(
        "--viz-only",
        action="store_true",
        help="Skip the table and run only the turtle visualization.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        nargs="+",
        default=None,
        metavar="N",
        help="Steps to highlight in table and animation (e.g. --steps 20 40 60 100).",
    )
    args = parser.parse_args()
    if args.table_only and args.viz_only:
        parser.error("Cannot use both --table-only and --viz-only.")
    return args


def main() -> None:
    args = _parse_args()
    steps_highlight = args.steps

    if not args.viz_only:
        print_comparison_table(steps_highlight=steps_highlight)

    if not args.table_only:
        try:
            run_turtle_visualization(steps_highlight=steps_highlight)
        except (KeyboardInterrupt, turtle.Terminator):
            pass
        except Exception as e:
            print(f"Visualization error: {e}")
            raise
        if not args.viz_only:
            input("\nPress Enter to close the simulation...")


if __name__ == "__main__":
    main()
