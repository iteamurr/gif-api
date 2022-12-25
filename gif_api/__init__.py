import os
from pathlib import Path


os.environ["PYTHONPATH"] = str(Path(__file__).parent.resolve())

__version__ = "0.1.0"

__all__ = ["__version__"]
