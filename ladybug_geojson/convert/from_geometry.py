# coding=utf-8
'''Functions to create GEOJSON geometry strings from Ladybug geometries.'''
import json
from typing import Optional
from .._validator import ( _Validator, 
    GeojSONTypes )
try:
    from ladybug_geometry.geometry2d.pointvector import Vector2D, Point2D
    from ladybug_geometry.geometry2d.arc import Arc2D
    from ladybug_geometry.geometry2d.polyline import Polyline2D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

def from_arc_2d(arc: Arc2D, 
    divisions: Optional[int]=20,
    validation: Optional[bool]=False) -> str:
    '''GEOJSON Polygon or LineString string from Ladybug Arc2D.
        If validation is active and there is an error it returns the error
    Mapping is
    - Closed Arc2D > Polygon 
    - Open Arc2D > LineString
    
    Args:
    - arc: ladybug Arc2D
    - divisions: number of divisions to use with polyline
    - validation: optional validation using GEOJSON schema
    '''
    poly = arc.to_polyline(divisions)
    vertices = [pt.to_array() for pt in poly.vertices]
    
    out = {}
    if arc.is_circle:
        # append the first vertices
        vertices.append(vertices[0])

        out = {
            "type": "Polygon", 
            "coordinates": [vertices]
        }
    else:
        out = {
            "type": "LineString", 
            "coordinates": vertices
        }
    json_string = json.dumps(out)

    if validation:
        validator = _Validator(json=json_string,
            target=[GeojSONTypes.LINESTRING, 
            GeojSONTypes.POLYGON])
        if validator.error:
            return validator.error

    return json_string