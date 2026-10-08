#!/usr/bin/env python3
"""Local check for Canvas target-list validation and CLI precedence; no API calls."""

import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/dot-device-openapi/scripts"))
from send_canvas import build_payload, validate_canvas_payload

with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", encoding="utf-8") as source:
    payload = {"taskType": "fixed", "data": {"taskType": "user data"}, "windowData": {"default": []}}
    json.dump(payload, source)
    source.flush()
    args = SimpleNamespace(payload=source.name, link=None, border=None, task_key=None, task_alias=None, task_type=None, refresh_now=None)
    assert build_payload(args)["taskType"] == "fixed"
    args.task_type = "loop"
    assert build_payload(args)["taskType"] == "loop"
    validate_canvas_payload(payload)
    payload.pop("taskType")
    validate_canvas_payload(payload)
    source.seek(0)
    source.truncate()
    json.dump(payload, source)
    source.flush()
    args.task_type = None
    assert "taskType" not in build_payload(args)
    for task_type in ("loop", "fixed"):
        validate_canvas_payload({**payload, "taskType": task_type})
    for task_type in (None, "other"):
        try:
            validate_canvas_payload({**payload, "taskType": task_type})
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted invalid taskType: {task_type!r}")
