"""Utilities for text formatting."""

import json
from typing import Any, Dict


def pformat_str_json(json_str: str) -> str:
    return json.dumps(json.loads(json_str), sort_keys=True, indent=4)


def pformat_json(json_dict: Dict[str, Any]) -> str:
    return json.dumps(json_dict, sort_keys=True, indent=4)
