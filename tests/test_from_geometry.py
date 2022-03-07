# coding=utf-8
import pytest
import json
import math

try:
    from ladybug_geometry.geometry2d.pointvector import Vector2D, Point2D
    from ladybug_geometry.geometry2d.arc import Arc2D
    from ladybug_geometry.geometry2d.polyline import Polyline2D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

from ladybug_geojson.convert.from_geometry import (
  from_arc_2d
)

def test_from_arc():
    arc = Arc2D(Point2D(0,0), 10)

    geojson_string = from_arc_2d(arc=arc, 
        divisions=4)
    first_pt = [10, 0]

    obj = json.loads(geojson_string)
    assert isinstance(obj, dict)
    assert obj.get('coordinates')[0][0] == first_pt