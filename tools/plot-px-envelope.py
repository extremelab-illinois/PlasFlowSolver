#!/usr/bin/env python3
"""
@file plot-px-envelope.py

@brief Utility for plotting the facility experimental bounds.

Copyright (C) 2023-2025 The Board of Trustees of the University of Illinois.
All rights reserved.

This file is part of PlasFlowSolver: data reduction model for ICP wind tunnels.

PlasFlowSolver is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

PlasFlowSolver is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with PlasFlowSolver.  If not, see
<http://www.gnu.org/licenses/>.
"""
from __future__ import annotations
import argparse
import csv
import sys
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def ensure_matplotlib():
    """Try to import matplotlib, with a friendly diagnostic on failure."""
    try:
        import matplotlib.pyplot as plt  # noqa: F401
    except ModuleNotFoundError:
        print(
            "System is missing `matplotlib` package required for plotting.\n"
            "You can install it with:\n"
            "    python -m pip install matplotlib\n"
        )
        raise SystemExit(1)


Point = Tuple[float, float]  # (P_kPa, q_Wcm2)


# Resolve user gas naming
def _pick_canonical(target: str, available: List[str]) -> Optional[str]:
    t = target.lower()
    for name in available:
        if name.lower() == t:
            return name
    return None


def resolve_gas_name_simple(mech_name: str, available_names) -> Optional[str]:
    """
    Map mechanism-like names to facility gas labels.

    Current rules:
      - CO2_* -> 'CO2'
      - any name containing 'air' -> 'Air'
      - nitrogen2, nitrogen5, test_N2, n2 -> 'N2'
    """
    s = mech_name.strip().lower()
    if s.endswith(".xml"):
        s = s[:-4]

    if s.startswith("co2"):
        return _pick_canonical("CO2", list(available_names))

    if "air" in s:
        return _pick_canonical("Air", list(available_names))

    if s in {"nitrogen2", "nitrogen5", "test_n2", "n2"}:
        return _pick_canonical("N2", list(available_names))

    # last resort: case-insensitive exact match to any available name
    return _pick_canonical(s, list(available_names))


# ---------- geometry ----------
def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: List[Point]) -> List[Point]:
    """Returns CCW hull without duplicate last point."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def point_on_segment(p: Point, a: Point, b: Point, eps: float = 1e-12) -> bool:
    (x, y), (x1, y1), (x2, y2) = p, a, b
    area2 = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
    if abs(area2) > eps * max(1.0, abs(x), abs(y),
                              abs(x1), abs(y1), abs(x2), abs(y2)):
        return False
    return (
        min(x1, x2) - eps <= x <= max(x1, x2) + eps
        and min(y1, y2) - eps <= y <= max(y1, y2) + eps
    )


def point_in_polygon(point: Point, poly: List[Point],
                     eps: float = 1e-12) -> bool:
    """Return True if point is inside or on the boundary of poly."""
    x, y = point
    n = len(poly)
    # boundary check
    for i in range(n):
        if point_on_segment(point, poly[i], poly[(i + 1) % n], eps):
            return True
    inside = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        if y < y1 or y >= y2:
            continue
        if y2 == y1:
            continue
        t = (y - y1) / (y2 - y1)
        xint = x1 + t * (x2 - x1)
        if xint > x + eps:
            inside = not inside
    return inside


# ---------- CSV ingest (facility schema: kPa & W/cm^2) ----------
def read_facility_csv(path: str) -> Dict[str, List[Point]]:
    """
    Read CSV with columns:
      plasma gas, stagnation pressure [kPa], heat flux [W/cm^2]
    Units are already in kPa and W/cm^2 (no conversion).
    Comment lines starting with '#' are ignored.
    """
    with open(path, newline="") as f:
        lines = [ln for ln in f.read().splitlines()
                 if not ln.lstrip().startswith("#")]
    rdr = csv.DictReader(lines)
    req = {"plasma gas", "stagnation pressure [kPa]", "heat flux [W/cm^2]"}
    if not rdr.fieldnames or not req.issubset(set(rdr.fieldnames)):
        raise SystemExit(
            "CSV must have columns: plasma gas, "
            "stagnation pressure [kPa], heat flux [W/cm^2]"
        )
    by_gas: Dict[str, List[Point]] = defaultdict(list)
    for r in rdr:
        gas = (r["plasma gas"] or "").strip()
        if not gas:
            continue
        P = float(str(r["stagnation pressure [kPa]"]).replace(",", ""))
        q = float(str(r["heat flux [W/cm^2]"]).replace(",", ""))
        by_gas[gas].append((P, q))
    return by_gas


def build_hulls(
    all_pts: Dict[str, List[Point]], gas_filter: Optional[List[str]]
) -> Tuple[List[str], Dict[str, List[Point]]]:
    """Return (gases_in_use, hulls dict)."""
    gases = sorted(all_pts.keys())

    if gas_filter:
        gases = []
        missing = []
        for g in gas_filter:
            resolved = resolve_gas_name_simple(g, all_pts.keys())
            if resolved:
                gases.append(resolved)
            else:
                missing.append(g)

        if missing:
            print(
                f"[plot] Note: requested gases not found in CSV: {missing}",
                file=sys.stderr,
            )

    hulls: Dict[str, List[Point]] = {}
    for gas in gases:
        pts = all_pts.get(gas, [])
        if not pts:
            print(f"[plot] Note: No evelope data points for gas ({gas})",
                  file=sys.stderr,)
            continue
        hulls[gas] = convex_hull(pts) if len(pts) >= 3 else pts

    return gases, hulls


# ---------- dump polygons ----------
def dump_polygons(
    gases: List[str],
    hulls: Dict[str, List[Point]],
    out_file: Optional[str] = None,
) -> None:
    """
    Dump ordered polygon vertices as CSV with columns:
      gas,vertex_index,stagnation_pressure_kPa,heat_flux_W_per_cm2
    """
    out = sys.stdout if out_file is None else open(out_file, "w", newline="")
    close_me = out is not sys.stdout
    try:
        print(
            "gas,vertex_index,stagnation_pressure_kPa,heat_flux_W_per_cm2",
            file=out,
        )
        for gas in gases:
            hull = hulls.get(gas, [])
            if not hull:
                print(f"[plot] Note: No hull found for gas ({gas})")
                continue
            for vidx, (P, q) in enumerate(hull):
                print(f"{gas},{vidx},{P:.10g},{q:.10g}", file=out)
    finally:
        if close_me:
            out.close()
            print(f"[plot] Dumped polygon vertices to {out_file}")


# ---------- plotting ----------
def plot_bounds(
    all_pts: Dict[str, List[Point]],
    gases: List[str],
    hulls: Dict[str, List[Point]],
    show_points: bool,
    fill_polys: bool,
    user: Optional[Tuple[str, float, float]],
    title: Optional[str],
    out: Optional[str],
) -> None:

    ensure_matplotlib()
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6))
    marker = "x" if show_points else None

    for gas in gases:
        hull = hulls[gas]

        if len(hull) >= 3:
            hx = [p[0] for p in hull] + [hull[0][0]]
            hy = [p[1] for p in hull] + [hull[0][1]]
            line, = plt.plot(hx, hy, label=gas, marker=marker)
            if fill_polys:
                col = line.get_color()
                plt.fill(hx, hy, facecolor=col, alpha=0.15, edgecolor=None)

    # Optional user point
    if user:
        user_gas_raw, PkPa, qWcm2 = user
        resolved = resolve_gas_name_simple(user_gas_raw, gases)
        lbl = f"user: {user_gas_raw}"
        color = None
        if resolved and resolved in hulls and len(hulls[resolved]) >= 3:
            inside = point_in_polygon((PkPa, qWcm2), hulls[resolved])
            lbl = f"user: {resolved} ({'inside' if inside else 'outside'})"
            # try to color-match the resolved gas polygon
            for line in plt.gca().get_lines():
                if line.get_label().startswith(resolved):
                    color = line.get_color()
                    break
        plt.scatter(
            [PkPa],
            [qWcm2],
            marker="*",
            s=150,
            edgecolor="k",
            facecolor=color,
            label=lbl,
            zorder=5,
        )

    plt.xlabel("Stagnation Pressure [kPa]")
    plt.ylabel("Heat Flux [W/cm²]")
    if title:
        plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2, fontsize=9)
    plt.tight_layout()

    if out:
        plt.savefig(out, dpi=200)
        print(f"[plot] Saved: {out}")
    else:
        plt.show()


# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(
        description=(
            "Plot or dump the PlasmatronX facility envelope.\n\n"
            "The CSV is expected to have columns:\n"
            "  plasma gas, stagnation pressure [kPa], heat flux [W/cm^2]\n\n"
            "Typical usage:\n"
            "  * Plot all gases with shaded polygons:\n"
            "      python tools/plot-px-envelope.py Envelope/"
            "CleanCSV/ptx_envelope_clean.csv\n"
            "  * Plot only N2 and overlay a user point:\n"
            "      python tools/plot-px-envelope.py Envelope/CleanCSV/"
            "ptx_envelope_clean.csv \\\n"
            "          --gas N2 --user-gas nitrogen5 --user-PkPa 5.0 "
            "--user-qWcm2 150\n"
            "  * Dump polygon vertices for Air to a CSV:\n"
            "      python tools/plot-px-envelope.py Envelope/CleanCSV/"
            "ptx_envelope_clean.csv \\\n"
            "          --gas Air --dump --dump-file air_polygon.csv "
            "--no-plot\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("csv", help="Bounds CSV path (facility schema).")
    parser.add_argument(
        "--gas",
        help="Comma-separated gas list, e.g. Air,N2,CO2 "
        "(default: all gases in CSV).",
    )
    parser.add_argument(
        "--out",
        help="Save figure to this file instead of showing (e.g. bounds.png).",
    )
    parser.add_argument("--title", help="Figure title (default: "
                        "'Facility Bounds').")
    parser.add_argument(
        "--no-points", action="store_true", help="Hide polygon vertex markers."
    )
    parser.add_argument(
        "--no-fill", action="store_true", help="Do not shade polygons "
        "(lines only)."
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Do not create a plot (useful with --dump / --dump-file).",
    )
    parser.add_argument(
        "--dump",
        action="store_true",
        help="Dump ordered polygon vertices as CSV to stdout "
        "(or --dump-file).",
    )
    parser.add_argument(
        "--dump-file",
        help="Write dumped polygon CSV to this file (implies --dump).",
    )

    parser.add_argument(
        "--user-gas",
        help=(
            "User input gas/mechanism (e.g., air_11, nitrogen2, test_N2). "
            "Resolved to a facility gas name for the overlay point."
        ),
    )
    parser.add_argument(
        "--user-PkPa", type=float, help="User stagnation pressure in kPa."
    )
    parser.add_argument(
        "--user-qWcm2", type=float, help="User heat flux in W/cm²."
    )

    args = parser.parse_args()

    all_pts = read_facility_csv(args.csv)

    gas_filter = None
    if args.gas:
        gas_filter = [g.strip() for g in args.gas.split(",") if g.strip()]

    gases, hulls = build_hulls(all_pts, gas_filter)

    # Dump mode
    if args.dump or args.dump_file:
        dump_polygons(gases, hulls, args.dump_file)

    # User point (optional)
    user = None
    if (
        args.user_gas is not None
        and args.user_PkPa is not None
        and args.user_qWcm2 is not None
    ):
        user = (args.user_gas, args.user_PkPa, args.user_qWcm2)
    elif any(
        v is not None for v in (args.user_gas, args.user_PkPa, args.user_qWcm2)
    ):
        print(
            "[plot] Incomplete --user-* triple provided; ignoring user point.",
            file=sys.stderr,
        )

    if (not ((hulls and gases) or user)):
        print("Nothing to plot!")
        return

    # Plot unless explicitly disabled
    if not args.no_plot:
        plot_bounds(
            all_pts,
            gases=gases,
            hulls=hulls,
            show_points=not args.no_points,
            fill_polys=not args.no_fill,
            user=user,
            title=args.title or "Facility Bounds",
            out=args.out,
        )


if __name__ == "__main__":
    main()
