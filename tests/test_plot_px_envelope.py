import os
import sys
import subprocess
from pathlib import Path


# Reuse example CSV content (kPa, W/cm^2)
CSV_TEXT = """plasma gas,stagnation pressure [kPa],heat flux [W/cm^2]
Air,10.103,536.5870236
Air,30.0456,444.6203745
Air,29.9463,213.7875552
Air,20.1893,39.39142084
Air,10.0452,17.68321134
Air,0.7265,9.383514002
Air,0.7157,9.415026001
Air,0.436,230.8351663
Air,1.0198,423.1972892
Air,2.5167,457.0941408
CO2,19.5467,36.77308484
CO2,0.6369,38.69822842
CO2,0.6327,46.51483053
CO2,0.8403,103.3409193
CO2,1.2792,189.3303254
CO2,1.7437,264.3717242
CO2,2.4887,334.2446305
CO2,10.0698,361.0583554
CO2,19.6313,328.0338656
CO2,24.784,283.4054512
CO2,25.5776,234.0766896
CO2,25.5802,134.835577
N2,7.0658,161.0268227
N2,1.173,23.96883371
N2,1.1029,26.68299744
N2,0.8364,37.46889853
N2,0.8453,40.56248125
N2,1.3875,227.6007938
N2,1.8881,260.1310493
"""


def _write_csv(tmp_path: Path) -> Path:
    path = tmp_path / "bounds.csv"
    path.write_text(CSV_TEXT)
    return path


def _plotter_script_path() -> Path:
    # tests/ directory -> repo root -> tools/plot-px-envelope.py
    this_file = Path(__file__).resolve()
    repo_root = this_file.parents[1]   # .../PlasFlowSolver
    script = repo_root / "tools" / "plot-px-envelope.py"
    assert script.exists(), f"plotter script not found at: {script}"
    return script


def test_plot_px_envelope_generates_png(tmp_path, monkeypatch):
    csv_path = _write_csv(tmp_path)
    out_path = tmp_path / "bounds_all.png"

    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"  # non-interactive backend for CI/headless

    script = _plotter_script_path()

    cmd = [
        sys.executable,
        str(script),
        str(csv_path),
        "--out",
        str(out_path),
    ]
    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"stderr:\n{result.stderr}"
    assert out_path.exists()
    assert out_path.stat().st_size > 0


def test_plot_px_envelope_user_point(tmp_path):
    csv_path = _write_csv(tmp_path)
    out_path = tmp_path / "bounds_n2_user.png"

    env = dict(os.environ)
    env["MPLBACKEND"] = "Agg"

    script = _plotter_script_path()

    cmd = [
        sys.executable,
        str(script),
        str(csv_path),
        "--gas", "N2",
        "--user-gas", "nitrogen2",
        "--user-PkPa", "1.173",
        "--user-qWcm2", "23.96883371",
        "--out", str(out_path),
    ]
    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"stderr:\n{result.stderr}"
    assert out_path.exists()
    assert out_path.stat().st_size > 0
