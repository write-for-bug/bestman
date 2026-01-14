# src/bestman/robots/startouch/interface_py/__init__.py
import importlib.util
import os
import glob

_here = os.path.dirname(__file__)
_candidates = glob.glob(os.path.join(_here, "_startouch.*.so"))

if not _candidates:
    raise ImportError("Startouch native module (.so) not found in interface_py/")

_spec = importlib.util.spec_from_file_location("startouch", _candidates[0])
startouch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(startouch)

__all__ = ["startouch"]