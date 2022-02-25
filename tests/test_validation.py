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

    valid = '''
    {
        "type": "MultiPoint", 
        "coordinates": [
            [10, 40, 0], [40, 30, 2], [20, 20, 4], [30, 10, 5]
        ]
    }'''

    validator = _Validator(valid, [GeojSONTypes.MULTIPOINT])
    assert validator.selection == GeojSONTypes.MULTIPOINT

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

    valid = '''{
        "type": "MultiLineString", 
        "coordinates": [
            [[10, 10], [20, 20], [10, 40]], 
            [[40, 40], [30, 30], [40, 20], [30, 10]]
        ]
    }'''
        
    invalid = '''{
        "type": "MultiLineString", 
        "coordinates": [
            [[10, 10]], 
            [[40, 40], [30, 30], [40, 20], [30, 10]]
        ]
    }'''
    
    validator = _Validator(valid, [GeojSONTypes.MULTILINESTRING])
    assert validator.selection == GeojSONTypes.MULTILINESTRING

    validator = _Validator(invalid, [GeojSONTypes.MULTILINESTRING])
    assert validator.selection != GeojSONTypes.MULTILINESTRING

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

    # polygon with hole
    valid = '''{
        "type": "MultiPolygon", 
        "coordinates": [
            [
                [[40, 40], [20, 45], [45, 30], [40, 40]]
            ], 
            [
                [[20, 35], [10, 30], [10, 10], [30, 5], [45, 20], [20, 35]], 
                [[30, 20], [20, 15], [20, 25], [30, 20]]
            ]
        ]
    }'''
    
    invalid = '''{
        "type": "MultiPolygon", 
        "coordinates": [
            [
                [[40, 40]]
            ], 
            [
                [[20, 35], [10, 30], [10, 10], [30, 5], [45, 20], [20, 35]], 
                [[30, 20], [20, 15], [20, 25], [30, 20]]
            ]
        ]
    }'''
    
    validator = _Validator(valid, [GeojSONTypes.MULTIPOLYGON])
    assert validator.selection == GeojSONTypes.MULTIPOLYGON

    validator = _Validator(invalid, [GeojSONTypes.MULTIPOLYGON])
    assert validator.selection != GeojSONTypes.MULTIPOLYGON

def test_json_multi_validation():
    valid = ''' {
    "type": "GeometryCollection",
    "geometries": [{
        "type": "Point",
        "coordinates": [100.0, 0.0]
    }, {
        "type": "LineString",
        "coordinates": [
        [101.0, 0.0],
        [102.0, 1.0]
        ]
    }]
    }
    '''
    
    invalid = ''' {
    "type": "GeometryCollection",
    "geometries": [{
        "type": "Point",
        "coordinates": [100.0]
    }, {
        "type": "LineString",
        "coordinates": [
        [101.0, 0.0],
        [102.0, 1.0]
        ]
    }]
    }
    '''
    
    validator = _Validator(valid, [GeojSONTypes.GEOMETRYCOLLECTION])
    assert validator.selection == GeojSONTypes.GEOMETRYCOLLECTION

    validator = _Validator(invalid, [GeojSONTypes.GEOMETRYCOLLECTION])
    assert validator.selection != GeojSONTypes.GEOMETRYCOLLECTION

def test_json_feature_validation():
    valid = '''{
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
           [11.1214686,46.0677385],[11.121466,46.0677511],[11.1213806,46.0681452],          
           [11.1213548,46.0682642],[11.1213115,46.0684385],[11.1212897,46.0685261],
           [11.1212678,46.0686443]
        ]
      },
      "properties": {
        "lanes": 1,
        "name": "Via Rodolfo Belenzani"
      }
    }
    '''
    
    invalid = ''' {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
           [11.1214686,46.0677385]
        ]
      },
      "properties": {
        "lanes": 1,
        "name": "Via Rodolfo Belenzani"
      }
    }
    '''
    
    validator = _Validator(valid, [GeojSONTypes.FEATURE])
    assert validator.selection == GeojSONTypes.FEATURE

    validator = _Validator(invalid, [GeojSONTypes.FEATURE])
    assert validator.selection != GeojSONTypes.FEATURE