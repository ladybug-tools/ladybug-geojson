# coding=utf-8
import pytest

import json
from ladybug_geojson._validator import _Validator

# https://geojson.org/schema/Point.json
# https://geojson.org/

to_validate = '{"type": "Point","coordinates": [125.6, 10.1]}'

def test_json_validation():
    validator = _Validator(to_validate)
    assert validator.is_valid == True