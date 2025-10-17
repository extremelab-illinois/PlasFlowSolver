# utils/facility_bounds.py
from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import csv
# import math

Point = Tuple[float, float]


@dataclass
class GasPolygon:
    gas: str
    vertices: List[Point]  # [(P, q), ...]

    def bbox(self):
        xs = [p for p, _ in self.vertices]
        ys = [q for _, q in self.vertices]
        return min(xs), min(ys), max(xs), max(ys)


def resolve_gas_name(input_gas_name: str) -> str:
    gas_name_map = {"air_11": "Air",
                    "air_13": "Air",
                    "air_5": "Air",
                    "nitrogen2": "N2",
                    "nitrogen5": "N2",
                    "test_N2": "N2",
                    "CO2_8": "CO2",
                    }
    facility_gas_name = None
    try:
        facility_gas_name = gas_name_map[input_gas_name]
    except Exception:
        pass
    return facility_gas_name


def _convex_hull(points: List[Point]) -> List[Point]:
    """Monotone chain convex hull (CCW, no duplicate last point)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _to_pa(v: float, unit: str) -> float:
    u = unit.strip().lower()
    if u in {"pa", "pascal", "pascals"}:
        return v
    if u == "kpa":
        return v * 1.0e3
    if u == "mpa":
        return v * 1.0e6
    if u == "bar":
        return v * 1.0e5
    raise ValueError(f"Unsupported pressure unit: {unit}")


def _to_wm2(v: float, unit: str) -> float:
    u = unit.strip().lower()
    if u in {"w/m^2", "w/m2", "w m-2"}:
        return v
    if u in {"kw/m^2", "kw/m2"}:
        return v * 1.0e3
    if u in {"mw/m^2", "mw/m2"}:
        return v * 1.0e6
    if u in {"w/cm^2", "w per cm^2", "w cm-2"}:
        return v * 1.0e4
    raise ValueError(f"Unsupported heat-flux unit: {unit}")


def load_bounds_csv(
    path: str,
    *,
    gas_col: str = "gas",
    p_col: str = "pressure_Pa",
    q_col: str = "heat_flux_W_m2",
    polygon_col: Optional[str] = None,    # allow named polygons (optional)
    vertex_id_col: Optional[str] = None,  # for vertex ordering  (optional)
    pressure_unit: str = "Pa",            # "kPa" from CSV
    heatflux_unit: str = "W/m^2",         # "W/cm^2" from CSV
) -> Dict[str, "GasPolygon"]:
    """
    Reads bounds and returns {gas: GasPolygon} with vertices ordered.
    - If `vertex_id_col` exists in the CSV and is provided, sorts by it.
    - Else, preserves file order if rows appear contiguous for that polygon.
    - If order is unknown/unreliable, constructs a convex hull for safety.
    - Units are normalized to Pa and W/m^2 based on the provided unit hints.
    """

    # Read all rows first
    with open(path, newline="") as f:
        raw = list(csv.DictReader(f))

    # Basic schema checks
    for required in (gas_col, p_col, q_col):
        if required not in (raw[0].keys() if raw else {}):
            raise ValueError(f"Missing CSV column: {required}")

    # Group rows by (gas, polygon) where polygon defaults to "0"
    from collections import defaultdict
    groups: Dict[Tuple[str, str], List[dict]] = defaultdict(list)
    for row in raw:
        gas = (row.get(gas_col) or "").strip()
        poly = (row.get(polygon_col) if polygon_col else "0")
        poly = (str(poly).strip() if poly is not None else "0")
        if not gas:
            # skip empty-gas rows silently
            continue
        groups[(gas, poly)].append(row)

    db: Dict[str, GasPolygon] = {}

    # Process each (gas, polygon)
    for (gas, poly), rows in groups.items():
        # Decide ordering strategy
        ordered_rows: List[dict]
        if vertex_id_col and vertex_id_col in rows[0]:
            try:
                ordered_rows = sorted(rows, key=lambda r:
                                      int(str(r[vertex_id_col]).strip()))
            except Exception:
                # Fallback to file order if vertex ids are messy
                ordered_rows = rows
        else:
            # No explicit ordering: we will compute a convex hull over points
            ordered_rows = rows

        # Build points with unit normalization
        pts: List[Point] = []
        for r in ordered_rows:
            # Convert to floats and normalize units
            P_in = float(str(r[p_col]).replace(",", "").strip())
            q_in = float(str(r[q_col]).replace(",", "").strip())
            P = _to_pa(P_in, pressure_unit)
            q = _to_wm2(q_in, heatflux_unit)
            pts.append((P, q))

        # Build hull unless order is provided
        use_hull = True
        if vertex_id_col and vertex_id_col in rows[0]:
            use_hull = False  # trust explicit order if provided

        verts = _convex_hull(pts) if use_hull else pts

        if len(verts) < 3:
            raise ValueError(f"Gas '{gas}' polygon needs ≥3 distinct vertices"
                             f" (got {len(verts)}).")

        # If multiple polygons per gas appear
        # might want to merge or keep the largest.
        # For now: keep the *largest* polygon by area per gas key.
        def _poly_area_ccw(vs: List[Point]) -> float:
            return 0.5 * sum(vs[i][0]*vs[(i+1) % len(vs)][1]
                             - vs[(i+1) % len(vs)][0]*vs[i][1]
                             for i in range(len(vs)))

        area = abs(_poly_area_ccw(verts))
        key = gas
        # keep max area polygon for this gas (common “outer envelope” case)
        if key not in db or area > abs(_poly_area_ccw(db[key].vertices)):
            db[key] = GasPolygon(gas=gas, vertices=verts)

        # Optional: warn if hull dropped interior points (concavity)
        if use_hull and len(verts) < len(set(pts)):
            print(f"[ptx envelope] Note: gas '{gas}' "
                  "had unordered/concave points; "
                  f"using convex hull with {len(verts)} vertices "
                  f"(from {len(set(pts))}).")

    return db


# ---------- Robust point-in-polygon (ray casting + boundary inclusion) -------
def _almost_equal(a: float, b: float, eps: float) -> bool:
    return abs(a - b) <= eps * max(1.0, abs(a), abs(b))


def _point_on_segment(p: Point, a: Point, b: Point, eps: float) -> bool:
    # Colinearity via cross product area ~ 0 and within segment bbox
    (x, y), (x1, y1), (x2, y2) = p, a, b
    area2 = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
    if not _almost_equal(area2, 0.0, eps):
        return False
    # within bounding rectangle (with tolerance)
    return (min(x1, x2) - eps <= x <= max(x1, x2) + eps and
            min(y1, y2) - eps <= y <= max(y1, y2) + eps)


def point_in_polygon(point: Point, poly: List[Point],
                     eps: float = 1e-12) -> bool:
    """
    True if inside or on boundary. Works for simple polygons (CW or CCW),
    convex or concave. No external deps.
    """
    x, y = point
    # Quick reject with bbox
    xs = [px for px, _ in poly]
    ys = [py for _, py in poly]
    if (x < min(xs) - eps or x > max(xs) + eps):
        return False
    if (y < min(ys) - eps or y > max(ys) + eps):
        return False

    # Boundary check
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if _point_on_segment((x, y), a, b, eps):
            return True

    # Ray cast horizontally to +inf
    inside = False
    for i in range(n):
        (x1, y1) = poly[i]
        (x2, y2) = poly[(i + 1) % n]

        # Ensure y1 <= y2
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        # Check if ray crosses edge (y in [y1, y2))
        if y < y1 or y >= y2:
            continue

        # Compute x intersection
        if _almost_equal(y1, y2, eps):  # horiz edge alrdy hndd by bnd check
            continue
        t = (y - y1) / (y2 - y1)
        xint = x1 + t * (x2 - x1)

        if xint > x + eps:
            inside = not inside
    return inside


def contains(db: Dict[str, GasPolygon], gas: str, P_Pa: float, q_W_m2: float,
             eps: float = 1e-12) -> bool:
    g = db.get(gas)
    if g is None:
        # If unknown gas, choose policy: treat as "out of bounds" (warn).
        print(f"WARNING: Gas '{gas}' not found in PTX testing envelope data.")
        return False
    return point_in_polygon((P_Pa, q_W_m2), g.vertices, eps)
