"""Probe: run capture.py with check_palette_mode's insert-point selector excluding the delete button."""
import inspect, sys, runpy
sys.path.insert(0, "test/visual")
import capture_comment_checks as c
src = inspect.getsource(c.check_palette_mode).replace(
  'insert-point--start) button")', 'insert-point--start) button:not(.sphinx-preview-delete)")')
assert src != inspect.getsource(c.check_palette_mode)
ns = c.__dict__
exec(src, ns)  # redefine in module namespace before capture imports it
sys.argv = ["capture.py", "--scenario", "palette-slash/v05-mode-strict-light-900", "--workers", "1"]
runpy.run_path("test/visual/capture.py", run_name="__main__")
