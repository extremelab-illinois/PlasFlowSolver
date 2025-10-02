# tests/conftest.py
import os
import sys
import pathlib
import pytest
import subprocess


def pytest_addoption(parser):
    parser.addoption(
        "--full", action="store_true", default=False,
        help="Run full/slow tests (or set env FULL_CI=1)."
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")

@pytest.fixture(scope="session")
def project_root():
    return pathlib.Path(__file__).resolve().parents[1]

@pytest.fixture
def runpy(project_root, monkeypatch, tmp_path):
    """
    Helper to run: python -m PlasFlowSolver.main (or plain main.py)
    Returns (rc, stdout, stderr).
    """
    def _run(*args, env=None, timeout=90):
        # Make source importable without installing a wheel
        cur = os.environ.copy()
        cur["PYTHONPATH"] = f"{project_root}:{cur.get('PYTHONPATH','')}"
        if env:
            cur.update(env)
        # Prefer module run so relative imports work even if main is in a package
        cmd = [sys.executable, "-m", "main"]  # adjust to "PlasFlowSolver.main" if you package it
        cmd += list(args)
        proc = subprocess.run(
            cmd, cwd=tmp_path, env=cur,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr
    return _run

@pytest.fixture(scope="session")
def is_full(request):
    return bool(os.environ.get("FULL_CI")) or request.config.getoption("--full")
