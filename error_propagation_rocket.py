"""
Computational Lab Assignment: Error propagation in π approximation.

Uses a formula that CALCULATES π (Leibniz/Gregory series). The baselines 3.1415 and 3.1416
are the truncated vs rounded values to 4 decimal places. The script shows the value of π
at the 20th, 40th, 60th, and 100th term of the series for both baselines and the gap between them.

Rocket visualization: two rockets are driven by pi from Leibniz at each step (trunc vs round).
Run with Python for table + rockets; --viz for rockets only.
"""

import argparse
import math
import time
from typing import List, Optional

# Terms at which we report (assignment: 20th, 40th, 60th, 100th)
STEPS = [20, 40, 60, 100]
DECIMAL_PLACES = 4
MAX_STEP = 100
ANGLE_DIVISOR = 50.0
SCALE = 3.5
VISUAL_AMPLIFICATION = 500
STEP_DELAY = 0.05
STOP_AT_STEP_SEC = 0.8


def compute_pi_leibniz(n_terms: int) -> float:
    """
    Compute π using the Leibniz/Gregory series: π/4 = 1 - 1/3 + 1/5 - 1/7 + ...

    This is a formula that CALCULATES π (as required by the assignment).

    Args:
        n_terms: Number of terms to sum.

    Returns:
        Approximation of π after n_terms.
    """
    if n_terms <= 0:
        raise ValueError(f"n_terms must be positive, got {n_terms}")
    total = 0.0
    for k in range(n_terms):
        total += (-1) ** k / (2 * k + 1)
    return 4.0 * total


def truncate_to_n_decimals(value: float, n: int) -> float:
    """Truncate value to n decimal places (baseline 1: 3.1415 style)."""
    factor = 10 ** n
    return int(value * factor) / factor


def round_to_n_decimals(value: float, n: int) -> float:
    """Round value to n decimal places (baseline 2: 3.1416 style)."""
    return round(value, n)


def rocket_vector_magnitude(pi_value: float, step: int) -> float:
    """Rocket diagonal magnitude sqrt((pi*step)^2 + step^2); used to show propagation of pi error."""
    return math.sqrt((pi_value * step) ** 2 + step**2)


def print_comparison_table(
    steps_highlight: Optional[List[int]] = None,
    precision: int = 15,
) -> None:
    """
    Print the assignment table: at the 20th, 40th, 60th, 100th term of the Leibniz series,
    show partial π, truncated (4 dec), rounded (4 dec), and the gap between the two baselines.
    """
    steps = steps_highlight if steps_highlight is not None else STEPS
    n_dec = DECIMAL_PLACES
    col_term = "Term"
    col_partial = "Partial pi"
    col_trunc = "Trunc (4 dec)"
    col_round = "Round (4 dec)"
    col_gap = "Gap"

    w_term = 6
    w_val = max(20, precision + 6)
    w_gap = max(14, precision)

    print("\n--- Error Propagation: pi from Leibniz Series (Truncated vs Rounded Baseline) ---")
    print("Formula that calculates pi: pi/4 = 1 - 1/3 + 1/5 - 1/7 + ... (Leibniz)")
    print("Baselines: 3.1415 (truncate to 4 dec) and 3.1416 (round to 4 dec).")
    print("Table shows the 20th, 40th, 60th, 100th term: partial pi and the gap between the two baselines.\n")

    header = f"{col_term:<{w_term}} | {col_partial:<{w_val}} | {col_trunc:<{w_val}} | {col_round:<{w_val}} | {col_gap:<{w_gap}}"
    separator = "-" * len(header)
    print(header)
    print(separator)

    for term in sorted(steps):
        partial = compute_pi_leibniz(term)
        trunc_val = truncate_to_n_decimals(partial, n_dec)
        round_val = round_to_n_decimals(partial, n_dec)
        gap = abs(round_val - trunc_val)
        print(
            f"{term:<{w_term}} | {partial:<{w_val}.{precision}f} | {trunc_val:<{w_val}.{n_dec}f} | "
            f"{round_val:<{w_val}.{n_dec}f} | {gap:<{w_gap}.{precision}f}"
        )

    print(separator)
    print()


def run_rocket_visualization(
    steps_highlight: Optional[List[int]] = None,
    max_step: int = MAX_STEP,
) -> None:
    """
    Rocket visualization driven by Leibniz: at each step n, pi comes from the nth term
    (truncated vs rounded to 4 decimals). Green rocket = trunc baseline, cyan = round baseline.
    """
    try:
        import turtle
    except ImportError:
        print("Turtle not available; run with --table-only to see the table.")
        return

    steps = steps_highlight if steps_highlight is not None else STEPS
    screen = turtle.Screen()
    screen.setup(900, 700)
    screen.bgcolor("#0a0a0f")
    screen.title("Rocket - pi from Leibniz (Trunc vs Round)")
    screen.setworldcoordinates(-380, -380, 380, 380)
    turtle.tracer(0)

    def position_from_angle(angle_rad: float, s: int) -> tuple:
        radius = s * SCALE
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
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
        f"{'Term':>4}   —   {'Vec (trunc)':>18}   —   {'Vec (round)':>18}   —   {'Gap':>18}",
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
        # Pi at this step from Leibniz (trunc vs round to 4 dec) — rockets connected to Leibniz
        partial = compute_pi_leibniz(step)
        pi_trunc = truncate_to_n_decimals(partial, DECIMAL_PLACES)
        pi_round = round_to_n_decimals(partial, DECIMAL_PLACES)

        angle_trunc = pi_trunc * step / ANGLE_DIVISOR
        angle_round_true = pi_round * step / ANGLE_DIVISOR
        angle_round_visual = angle_trunc + (angle_round_true - angle_trunc) * VISUAL_AMPLIFICATION

        pos_trunc = position_from_angle(angle_trunc, step)
        pos_round = position_from_angle(angle_round_visual, step)

        t1.goto(pos_trunc)
        t2.goto(pos_round)

        turtle.update()
        time.sleep(STEP_DELAY)

        if step in steps:
            vec_trunc = rocket_vector_magnitude(pi_trunc, step)
            vec_round = rocket_vector_magnitude(pi_round, step)
            gap = abs(vec_round - vec_trunc)
            value_line.clear()
            value_line.write(
                f"{int(step):>4}   —   {vec_trunc:>18.10f}   —   {vec_round:>18.10f}   —   {gap:>18.10f}",
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
    label1.write("Trunc (Leibniz)", align="right", font=("Arial", 14, "bold"))
    label2 = turtle.Turtle()
    label2.hideturtle()
    label2.penup()
    label2.color("#00ccff")
    label2.goto(t2.xcor() - 12, t2.ycor())
    label2.write("Round (Leibniz)", align="right", font=("Arial", 14, "bold"))

    turtle.tracer(1)
    turtle.exitonclick()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Computational lab: π from Leibniz series; compare trunc vs round baseline at 20, 40, 60, 100.",
    )
    parser.add_argument(
        "--table-only",
        action="store_true",
        help="Print the comparison table and exit (no visualization).",
    )
    parser.add_argument(
        "--viz",
        action="store_true",
        help="Show rocket visualization (pi from Leibniz at each step; trunc vs round).",
    )
    parser.add_argument(
        "--steps",
        type=int,
        nargs="+",
        default=None,
        metavar="N",
        help="Terms to report (default: 20 40 60 100).",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    args = _parse_args()
    steps = args.steps

    if not args.viz:
        print_comparison_table(steps_highlight=steps)

    if args.viz or not args.table_only:
        if not args.table_only and not args.viz:
            run_rocket_visualization(steps_highlight=steps)
        elif args.viz:
            run_rocket_visualization(steps_highlight=steps)

    if not args.table_only and not args.viz:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
