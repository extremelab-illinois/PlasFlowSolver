import pytest
import utils.facility_bounds as fb

# Realistic N2 snippet (kPa, W/cm^2)
N2_CSV = """plasma gas,stagnation pressure [kPa],heat flux [W/cm^2]
N2,7.0658,161.0268227
N2,1.173,23.96883371
N2,1.1029,26.68299744
N2,0.8364,37.46889853
N2,0.8453,40.56248125
N2,1.3875,227.6007938
N2,1.8881,260.1310493
"""


def test_resolve_gas_name_mapping():
    # Uses your explicit map in facility_bounds.resolve_gas_name
    assert fb.resolve_gas_name("air_11") == "Air"
    assert fb.resolve_gas_name("air_13") == "Air"
    assert fb.resolve_gas_name("air_5") == "Air"
    assert fb.resolve_gas_name("nitrogen2") == "N2"
    assert fb.resolve_gas_name("nitrogen5") == "N2"
    assert fb.resolve_gas_name("test_N2") == "N2"
    assert fb.resolve_gas_name("CO2_8") == "CO2"
    # Unknown should return None
    assert fb.resolve_gas_name("Mars_19") is None


def _load_n2_polygon(tmp_path):
    path = tmp_path / "n2_bounds.csv"
    path.write_text(N2_CSV)
    db = fb.load_bounds_csv(
        str(path),
        gas_col="plasma gas",
        p_col="stagnation pressure [kPa]",
        q_col="heat flux [W/cm^2]",
        pressure_unit="kPa",
        heatflux_unit="W/cm^2",
        polygon_col=None,
        vertex_id_col=None,
    )
    assert "N2" in db
    return db["N2"]


def test_envelope_diagnostics_inside_vertex(tmp_path):
    """
    Pick a known vertex of the N2 polygon; diagnostics should:
      - report inside_polygon=True
      - show no violations
      - bounds enclosing the point.
    """
    gas_poly = _load_n2_polygon(tmp_path)

    # Use one of the vertices directly
    P_kPa = 1.173
    q_Wcm2 = 23.96883371

    diag = fb.envelope_diagnostics(gas_poly, P_kPa*1e3, q_Wcm2*1e4)

    assert diag.gas == "N2"
    assert diag.inside_polygon
    assert not diag.pressure_violation
    assert not diag.heatflux_violation

    assert diag.Pmin_kPa <= P_kPa <= diag.Pmax_kPa
    assert diag.qmin_Wcm2 <= q_Wcm2 <= diag.qmax_Wcm2

    assert diag.dP_kPa == pytest.approx(0.0)
    assert diag.dq_Wcm2 == pytest.approx(0.0)


def test_envelope_diagnostics_outside_high(tmp_path):
    """
    Choose a point well above the N2 envelope; diagnostics should show
    violations and positive distances in both dimensions.
    """
    gas_poly = _load_n2_polygon(tmp_path)

    # Clearly outside in both pressure and heat flux
    P_kPa = 100.0
    q_Wcm2 = 1000.0

    diag = fb.envelope_diagnostics(gas_poly, P_kPa*1e3, q_Wcm2*1e4)

    assert not diag.inside_polygon
    assert diag.pressure_violation
    assert diag.heatflux_violation

    assert diag.dP_kPa > 0.0
    assert diag.dq_Wcm2 > 0.0

    # should be above the max bounds
    assert P_kPa > diag.Pmax_kPa
    assert q_Wcm2 > diag.qmax_Wcm2

import math
from utils.facility_bounds import (
    GasPolygon,
    envelope_diagnostics,
)


def test_polygon_boundary_distance_outside_square():
    """
    Point is outside a square polygon.
    Verify:
      - inside_polygon is False
      - closest-point deltas move toward the polygon
      - normalized distance is positive
    """
    # Square in (kPa, W/cm^2) mapped internally to SI
    # Square corners: (1,1), (3,1), (3,3), (1,3)
    poly = GasPolygon(
        gas="TEST",
        vertices=[
            (1.0e3, 1.0e4),
            (3.0e3, 1.0e4),
            (3.0e3, 3.0e4),
            (1.0e3, 3.0e4),
        ],
    )

    # Point clearly outside: right and above
    P = 4.0e3
    q = 4.0e4
    P_kPa = 4.0
    q_Wcm2 = 4.0

    diag = envelope_diagnostics(poly, P, q)

    assert not diag.inside_polygon
    assert diag.dist_poly_norm > 0.0

    # Closest point should pull us back toward the square
    # Expect negative deltas in both components
    assert diag.dP_poly_kPa < 0.0
    assert diag.dq_poly_Wcm2 < 0.0

    # Applying the deltas should land us on or very near the boundary
    P_new = (P_kPa + diag.dP_poly_kPa)*1.e3
    q_new = (q_Wcm2 + diag.dq_poly_Wcm2)*1.e4

    diag2 = envelope_diagnostics(poly, P_new, q_new)
    assert diag2.dist_poly_norm < 1.0e-12


def test_polygon_boundary_distance_on_edge_is_zero():
    """
    Point lies exactly on a polygon edge.
    Expect:
      - inside_polygon may be True or False depending on winding,
        but boundary distance must be zero.
    """
    poly = GasPolygon(
        gas="TEST",
        vertices=[
            (0.0, 0.0),
            (2.0e3, 0.0),
            (2.0e3, 2.0e4),
            (0.0, 2.0e4),
        ],
    )

    # Exactly on right edge
    P = 2.0e3
    q = 1.0e4

    diag = envelope_diagnostics(poly, P, q)

    assert math.isclose(diag.dist_poly_norm, 0.0, abs_tol=1.0e-12)
    assert math.isclose(diag.dP_poly_kPa, 0.0, abs_tol=1.0e-12)
    assert math.isclose(diag.dq_poly_Wcm2, 0.0, abs_tol=1.0e-12)
