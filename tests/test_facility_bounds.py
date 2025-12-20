import utils.facility_bounds as fb


def square():
    return [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]


def test_inside():
    assert fb.point_in_polygon((1.0, 1.0), square())


def test_edge_is_inside():
    assert fb.point_in_polygon((0.0, 1.0), square())


def test_outside():
    assert not fb.point_in_polygon((3.0, 1.0), square())


def test_contains_by_gas():
    db = {"Air": fb.GasPolygon(gas="Air", vertices=square())}
    assert fb.contains(db, "Air", 1.0, 1.0)
    assert not fb.contains(db, "Air", -1.0, 1.0)
    assert not fb.contains(db, "Unknown", 1.0, 1.0)  # unknown gas -> outside


CSV = """plasma gas,stagnation pressure [kPa],heat flux [W/cm^2]
N2,7.0658,161.0268227
N2,1.173,23.96883371
N2,1.1029,26.68299744
N2,0.8364,37.46889853
N2,0.8453,40.56248125
N2,1.3875,227.6007938
N2,1.8881,260.1310493
"""


def test_n2_realdata_convex_hull_and_membership(tmp_path):
    path = tmp_path / "n2_bounds.csv"
    path.write_text(CSV)

    db = fb.load_bounds_csv(
        str(path),
        gas_col="plasma gas",
        p_col="stagnation pressure [kPa]",
        q_col="heat flux [W/cm^2]",
        pressure_unit="kPa",     # kPa -> Pa
        heatflux_unit="W/cm^2",  # W/cm^2 -> W/m^2
        polygon_col=None,
        vertex_id_col=None,
    )
    assert "N2" in db
    poly = db["N2"].vertices
    assert isinstance(poly, list) and len(poly) >= 3

    # Original points in native units (kPa, W/cm^2)
    raw_pts = [
        (7.0658, 161.0268227),
        (1.173, 23.96883371),
        (1.1029, 26.68299744),
        (0.8364, 37.46889853),
        (0.8453, 40.56248125),
        (1.3875, 227.6007938),
        (1.8881, 260.1310493),
    ]
    # Convert to SI like the loader: Pa and W/m^2
    si_pts = [(P_kPa * 1e3, q_Wcm2 * 1e4) for (P_kPa, q_Wcm2) in raw_pts]

    # Each original data point should be inside/on the polygon
    for P_pa, q_wm2 in si_pts:
        assert fb.point_in_polygon((P_pa, q_wm2), poly), \
            f"Point {(P_pa, q_wm2)} not in polygon"

    # Basic unit conversion sanity via bbox (min/max should bracket our data)
    xs = [x for x, _ in poly]
    ys = [y for _, y in poly]
    minP, maxP = min(xs), max(xs)
    minq, maxq = min(ys), max(ys)
    rawP = [p for (p, _) in si_pts]
    rawq = [q for (_, q) in si_pts]
    assert minP <= min(rawP) + 1e-9 and maxP >= max(rawP) - 1e-9
    assert minq <= min(rawq) + 1e-6 and maxq >= max(rawq) - 1e-6

    # A clearly outside point (pressure way above max, heat flux above max)
    assert not fb.contains(
        db, "N2",
        P_Pa=maxP * 10.0,
        q_W_m2=maxq * 10.0,
    )
