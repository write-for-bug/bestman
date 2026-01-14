# src/bestman/robots/startouch/startouch_sdk/__init__.py
import importlib.util
import os
import glob

_here = os.path.dirname(__file__)

# 查找 Python 扩展模块（匹配 cpython-... 格式）
_candidates = glob.glob(os.path.join(_here, "startouch.*cpython*.so"))

if not _candidates:
    # 兼容其他平台（可选）
    _candidates = (
        glob.glob(os.path.join(_here, "startouch.*.so")) +
        glob.glob(os.path.join(_here, "startouch.*.dylib")) +
        glob.glob(os.path.join(_here, "startouch.*.pyd"))
    )
    # 过滤掉 libstartouch.so
    _candidates = [f for f in _candidates if 'libstartouch' not in os.path.basename(f)]

if not _candidates:
    raise ImportError(
        "Startouch native Python module (.so/.dylib/.pyd) not found. "
        "Expected file like 'startouch.cpython-310-x86_64-linux-gnu.so'."
    )

_module_path = _candidates[0]

_spec = importlib.util.spec_from_file_location("startouch", _module_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Failed to load module spec from {os.path.basename(_module_path)}")

startouch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(startouch)

from .startouchclass import SingleArm
# __all__ = ["startouch"]