# tests/test_00_smoke.py
def test_import_mutationpp():
    import mutationpp as mpp
    # Some packages don't export __version__; fall back to importlib.metadata.
    ver = getattr(mpp, "__version__", None)
    if not ver:
        try:
            from importlib.metadata import version
            ver = version("mutationpp")
        except Exception:
            ver = None
    assert isinstance(ver, str) and len(ver) > 0

# def test_import_plasflowsolver():
#    import importlib
#    # Adjust as needed if your top-level package name is different
#    mod = importlib.import_module("main")
#    assert mod is not None
