# coding=utf-8
import pytest

import json
from ladybug_geojson.to_geometry import ( to_vector2d,
    to_point2d,
    to_point3d, 
    to_vector3d )

try:
    from ladybug_geometry.geometry2d.pointvector import Vector2D, Point2D
    from ladybug_geometry.geometry2d.ray import Ray2D
    from ladybug_geometry.geometry2d.line import LineSegment2D
    from ladybug_geometry.geometry2d.polyline import Polyline2D
    from ladybug_geometry.geometry2d.polygon import Polygon2D
    from ladybug_geometry.geometry2d.mesh import Mesh2D
    from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
    from ladybug_geometry.geometry3d.ray import Ray3D
    from ladybug_geometry.geometry3d.line import LineSegment3D
    from ladybug_geometry.geometry3d.polyline import Polyline3D
    from ladybug_geometry.geometry3d.plane import Plane
    from ladybug_geometry.geometry3d.mesh import Mesh3D
    from ladybug_geometry.geometry3d.face import Face3D
    from ladybug_geometry.geometry3d.polyface import Polyface3D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

def test_geojson_to_vector():
    valid_2d = '{"type": "Point","coordinates": [125.6, 10.1]}'
    valid_3d = '{"type": "Point","coordinates": [125.6, 10.1, 10.5]}'

    vec_2d = to_vector2d(valid_2d)
    assert vec_2d is not None
    assert type(vec_2d) == Vector2D
    assert vec_2d == Vector2D(125.6, 10.1)

    vec_3d = to_vector3d(valid_3d)
    assert vec_3d is not None
    assert type(vec_3d) == Vector3D
    assert vec_3d == Vector3D(125.6, 10.1, 10.5)

def test_geojson_to_point():
    valid_2d = '{"type": "Point","coordinates": [125.6, 10.1]}'
    valid_3d = '{"type": "Point","coordinates": [125.6, 10.1, 10.5]}'

    pt_2d = to_point2d(valid_2d)
    assert pt_2d is not None
    assert type(pt_2d) == Point2D
    assert pt_2d == Point2D(125.6, 10.1)

    pt_3d = to_point3d(valid_3d)
    assert pt_3d is not None
    assert type(pt_3d) == Point3D
    assert pt_3d == Point3D(125.6, 10.1, 10.5)