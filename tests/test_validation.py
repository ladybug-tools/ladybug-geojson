# coding=utf-8
import pytest

import json
from ladybug_geojson._validator import _Validator

# https://geojson.org/schema/Point.json
# https://geojson.org/

def test_json_validation():
    valid = '{"type": "Point","coordinates": [125.6, 10.1]}'
    invalid = '{"type": "Point"}'

    validator = _Validator(valid)
    assert validator.is_valid == True

    validator = _Validator(invalid)
    assert validator.is_valid != True