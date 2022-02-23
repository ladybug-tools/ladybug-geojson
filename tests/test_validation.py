# coding=utf-8
import pytest

import json
from ladybug_geojson._validator import ( _Validator,
    GeojSONTypes )

# https://geojson.org/schema/Point.json
# https://geojson.org/

def test_json_point_validation():
    valid = '{"type": "Point","coordinates": [125.6, 10.1]}'
    invalid = '{"type": "Point"}'

    validator = _Validator(valid, [GeojSONTypes.POINT])
    assert validator.selection == GeojSONTypes.POINT

    validator = _Validator(invalid, [GeojSONTypes.POINT])
    assert validator.selection != GeojSONTypes.POINT

    valid = '''
    {
        "type": "MultiPoint", 
        "coordinates": [
            [10, 40], [40, 30], [20, 20], [30, 10]
        ]
    }
    '''
    invalid = '''
    {
        "type": "MultiPoint", 
        "coordinates": [
            [10]
        ]
    }'''

    validator = _Validator(valid, [GeojSONTypes.MULTIPOINT])
    assert validator.selection == GeojSONTypes.MULTIPOINT

    validator = _Validator(invalid, [GeojSONTypes.MULTIPOINT])
    assert validator.selection != GeojSONTypes.MULTIPOINT

def test_json_linestring_validation():
    valid = '''{"type": "LineString", 
        "coordinates":[[11.1212678, 46.0686443],
        [11.1212316,46.0688409]]}'''
    
    invalid = '''{"type": "LineString", 
    "coordinates":[[11.1212316,46.0688409]]}'''
    
    validator = _Validator(valid, [GeojSONTypes.LINESTRING])
    assert validator.selection == GeojSONTypes.LINESTRING

    validator = _Validator(invalid, [GeojSONTypes.LINESTRING])
    assert validator.selection != GeojSONTypes.LINESTRING

def test_json_polygon_validation():
    # polygon with hole
    valid = '''{
        "type": "Polygon", 
        "coordinates": [
            [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]], 
            [[20, 30], [35, 35], [30, 20], [20, 30]]
        ]
    }'''
    
    invalid = '''{
    "type": "Polygon", 
        "coordinates": [
            [[35, 10], [45, 45], [15, 40]]
        ]
    }'''
    
    validator = _Validator(valid, [GeojSONTypes.POLYGON])
    assert validator.selection == GeojSONTypes.POLYGON

    validator = _Validator(invalid, [GeojSONTypes.POLYGON])
    assert validator.selection != GeojSONTypes.POLYGON