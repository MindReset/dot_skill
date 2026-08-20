"""Bootstrap the shared dot_mcp package for direct script execution."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable


PACKAGE_ROOT = Path(__file__).resolve().parents[3]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from dot_mcp import DotClient, DotError  # noqa: E402


def run(operation: Callable[[], Any]) -> Any:
    try:
        return operation()
    except (DotError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
