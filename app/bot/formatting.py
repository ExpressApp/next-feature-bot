"""Utilities for text formatting."""

import json
from typing import Any, Dict


def pformat_str_json(json_str: str) -> str:
    return pformat_json(json.loads(json_str))


def pformat_json(json_dict: Dict[str, Any]) -> str:
    return json.dumps(json_dict, sort_keys=True, indent=4)
