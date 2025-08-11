
from pathlib import Path
import os
from pyprojroot import here

def create_directory(directory_path: str) -> Path:
    """
    Ensure a directory exists. If `directory_path` is relative, it's resolved
    against the project root (via `pyprojroot.here`). Absolute paths are used as-is.

    Returns:
        Path: the normalized directory path.
    """
    base = Path(directory_path)
    target = base if base.is_absolute() else Path(here(directory_path))

    target.mkdir(parents=True, exist_ok=True)
    return target
