"""Utilities for text formatting."""

import json


def pformat_str_json(json_str: str) -> str:
    return json.dumps(json.loads(json_str), sort_keys=True, indent=4)
