# coding=utf-8
import pytest

import json
from ladybug_geojson._validator import _Validator

# https://geojson.org/schema/Point.json
# https://geojson.org/

def test_json_point_validation():
    valid = '{"type": "Point","coordinates": [125.6, 10.1]}'
    invalid = '{"type": "Point"}'

    validator = _Validator(valid)
    assert validator.is_valid == True

    validator = _Validator(invalid)
    assert validator.is_valid != True

def test_json_linestring_validation():
    valid = '''{"type": "LineString", 
        "coordinates":[[11.1212678, 46.0686443],
        [11.1212316,46.0688409]]}'''
    
    invalid = '''{"type": "LineString", 
    "coordinates":[[11.1212316,46.0688409]]}'''
    
    validator = _Validator(valid)
    assert validator.is_valid == True

    validator = _Validator(invalid)
    assert validator.is_valid != True