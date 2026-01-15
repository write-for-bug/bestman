"""Startouch SDK loader with platform-specific binary support."""

import importlib.util
import os
import sys
import platform
import glob
from pathlib import Path

_here = Path(__file__).parent


def _find_binary():
    """Find the appropriate binary for current platform.
    
    First tries platform-specific directory structure:
    binaries/{system}-{machine}-py{version}/
    
    Falls back to old flat structure for backward compatibility.
    """
    system = platform.system().lower()
    machine = platform.machine()
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    
    # Try new platform-specific structure first
    platform_dir = _here / "binaries" / f"{system}-{machine}-py{py_version}"
    if platform_dir.exists():
        candidates = list(platform_dir.glob("startouch.*.so"))
        if candidates:
            return candidates[0]
    
    # Fallback to old structure (backward compatibility)
    # Look for Python extension module (cpython-... format)
    candidates = glob.glob(str(_here / "startouch.*cpython*.so"))
    
    if not candidates:
        # Try other formats
        candidates = (
            glob.glob(str(_here / "startouch.*.so")) +
            glob.glob(str(_here / "startouch.*.dylib")) +
            glob.glob(str(_here / "startouch.*.pyd"))
        )
        # Filter out libstartouch.so
        candidates = [f for f in candidates if 'libstartouch' not in os.path.basename(f)]
    
    if not candidates:
        raise ImportError(
            f"Startouch native Python module not found for platform "
            f"{system}-{machine}-py{py_version}. "
            f"Expected file like 'startouch.cpython-{py_version}-*.so' "
            f"or in 'binaries/{system}-{machine}-py{py_version}/' directory."
        )
    
    return Path(candidates[0])


def _load_module():
    """Dynamically load the startouch native module."""
    module_path = _find_binary()
    
    spec = importlib.util.spec_from_file_location("startouch", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(
            f"Failed to load module spec from {module_path.name}. "
            f"Full path: {module_path}"
        )
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load the native module
startouch = _load_module()

# Export the Python wrapper
from .startouchclass import SingleArm

__all__ = ["SingleArm", "startouch"]