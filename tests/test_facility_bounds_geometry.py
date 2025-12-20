import math
import pytest
import utils.facility_bounds as fb


def square():
    # Simple convex square in SI units
    # We'll feed directly to point_in_polygon
    return [
        (0.0, 0.0),
        (2.0, 0.0),
        (2.0, 2.0),
        (0.0, 2.0),
    ]


def test_point_in_polygon_inside():
    poly = square()
    assert fb.point_in_polygon((1.0, 1.0), poly)


def test_point_in_polygon_edge_is_inside():
    poly = square()
    assert fb.point_in_polygon((0.0, 1.0), poly)
    assert fb.point_in_polygon((1.0, 0.0), poly)


def test_point_in_polygon_outside():
    poly = square()
    assert not fb.point_in_polygon((3.0, 1.0), poly)
    assert not fb.point_in_polygon((-1.0, 1.0), poly)


def test_load_bounds_csv_facility_units_convex_hull(tmp_path):
    """
    Use a tiny synthetic facility-style CSV (kPa, W/cm^2) and verify that:
      - load_bounds_csv ingests it,
      - units are converted to SI (Pa, W/m^2),
      - and the polygon has the correct bounding box.
    """
    csv_text = """plasma gas,stagnation pressure [kPa],heat flux [W/cm^2]
N2,1.0,10.0
N2,3.0,10.0
N2,3.0,30.0
N2,1.0,30.0
"""
    path = tmp_path / "bounds.csv"
    path.write_text(csv_text)

    db = fb.load_bounds_csv(
        str(path),
        gas_col="plasma gas",
        p_col="stagnation pressure [kPa]",
        q_col="heat flux [W/cm^2]",
        pressure_unit="kPa",      # expect kPa -> Pa
        heatflux_unit="W/cm^2",   # expect W/cm^2 -> W/m^2
        polygon_col=None,
        vertex_id_col=None,
    )

    assert "N2" in db
    poly = db["N2"].vertices
    # We had 4 corner points; hull should also have 4 vertices
    assert len(poly) == 4

    xs = [P for (P, _) in poly]
    ys = [q for (_, q) in poly]

    # pressure: 1–3 kPa -> 1e3–3e3 Pa
    assert min(xs) == pytest.approx(1.0e3)
    assert max(xs) == pytest.approx(3.0e3)

    # heat flux: 10–30 W/cm^2 -> 1e5–3e5 W/m^2
    assert min(ys) == pytest.approx(10.0e4)
    assert max(ys) == pytest.approx(30.0e4)
