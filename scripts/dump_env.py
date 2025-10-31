"""Dump installed distributions in a pip-freeze style format.

This script uses importlib.metadata to list installed distributions and prints
one-per-line as Name==version. Useful when pip isn't available in the venv.
"""
import sys
try:
    import importlib.metadata as m
except Exception:
    try:
        import importlib_metadata as m
    except Exception:
        print("ERROR: importlib.metadata not available", file=sys.stderr)
        sys.exit(2)

dists = sorted(m.distributions(), key=lambda d: (d.metadata.get('Name') or '').lower())
for d in dists:
    name = d.metadata.get('Name') or d.metadata.get('Summary') or ''
    if not name:
        # fallback to distribution name
        name = d.metadata.get('Name') or d._path.name
    print(f"{name}=={d.version}")
