# coding=utf-8
from typing import List
import pytest

import json
from ladybug_geojson.to_geometry import ( 
    to_vector2d,
    to_point2d,
    to_point3d, 
    to_vector3d,
    to_linesegment2d,
    to_polyline2d,
    to_linesegment3d,
    to_polyline3d,
    to_polygon2d,
    to_face3d )

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

    multi_valid = '''
    {
        "type": "MultiPoint", 
        "coordinates": [
            [10, 40], [40, 30], [20, 20], [30, 10]
        ]
    }
    '''
    vec_2d = to_vector2d(multi_valid)
    assert vec_2d is not None
    assert type(vec_2d) == list
    assert vec_2d == [
        Vector2D(10, 40),
        Vector2D(40, 30),
        Vector2D(20, 20),
        Vector2D(30, 10)
    ]

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

    multi_valid = '''
    {
        "type": "MultiPoint", 
        "coordinates": [
            [10, 40], [40, 30], [20, 20], [30, 10]
        ]
    }
    '''
    pt_2d = to_point2d(multi_valid)
    assert pt_2d is not None
    assert type(pt_2d) == list
    assert pt_2d == [
        Point2D(10, 40),
        Point2D(40, 30),
        Point2D(20, 20),
        Point2D(30, 10)
    ]

def test_geojson_to_linesegment():
    valid_2d = '''{
        "type": "LineString", 
        "coordinates": [
            [11.1212678, 46.0686443],[11.1212316,46.0688409]
        ]
    }'''

    valid_long_2d = '''{
        "type": "LineString", 
        "coordinates": [
            [11.1212678, 46.0686443],[11.1212316,46.0688409], 
            [11.1212400, 46.0700000]
        ]
    }'''

    ln_2d = to_linesegment2d(valid_2d)
    assert ln_2d is not None
    assert type(ln_2d) == LineSegment2D
    assert ln_2d == LineSegment2D \
        .from_end_points(Point2D(11.1212678, 46.0686443),
        Point2D(11.1212316, 46.0688409))
    
    # test linesegment if input > 2 pts
    ln_cut_2d = to_linesegment2d(valid_long_2d)
    assert ln_cut_2d is not None
    assert type(ln_cut_2d) == LineSegment2D
    assert ln_cut_2d == LineSegment2D \
        .from_end_points(Point2D(11.1212678, 46.0686443),
        Point2D(11.1212400, 46.0700000))
    
    valid_3d = '''{
        "type": "LineString", 
        "coordinates": [
            [11.1212678, 46.0686443, 1],[11.1212316,46.0688409, 2]
        ]
    }''' 

    ln_3d = to_linesegment3d(valid_3d)
    assert ln_3d is not None
    assert type(ln_3d) == LineSegment3D
    assert ln_3d.p1 == Point3D(11.1212678, 46.0686443, 1)

    # it will use first and last point
    multi_valid_2d = '''{
        "type": "MultiLineString", 
        "coordinates": [
            [[10, 10], [20, 20], [10, 40]], 
            [[40, 40], [30, 30], [40, 20], [30, 10]]
        ]
    }'''

    ln_2d = to_linesegment2d(multi_valid_2d)
    assert ln_2d is not None
    assert type(ln_2d) == list
    assert ln_2d == [LineSegment2D \
        .from_end_points(Point2D(10, 10),
        Point2D(10, 40)),
        LineSegment2D \
        .from_end_points(Point2D(40, 40),
        Point2D(30, 10))]


def test_geojson_to_polyline():
    valid_2d = '''{
        "type": "LineString", 
        "coordinates": [
            [11.1212678, 46.0686443],[11.1212316,46.0688409], 
            [11.1212400, 46.0700000]
        ]
    }'''

    pl_2d = to_polyline2d(valid_2d)
    assert pl_2d is not None
    assert type(pl_2d) == Polyline2D
    assert pl_2d == Polyline2D(vertices=[
            Point2D(11.1212678, 46.0686443),
            Point2D(11.1212316,46.0688409),
            Point2D(11.1212400, 46.0700000)])
        
    pl_2d = to_polyline2d(valid_2d, 
        interpolated=True)
    assert pl_2d.interpolated == True
    
    valid_2d = '''{
        "type": "LineString", 
        "coordinates": [
            [11.1212678, 46.0686443],[11.1212316,46.0688409]
        ]
    }'''

    pl_2d = to_polyline2d(valid_2d)
    assert pl_2d is not None
    assert type(pl_2d) == LineSegment2D
    assert pl_2d == LineSegment2D \
        .from_end_points(Point2D(11.1212678, 46.0686443),
        Point2D(11.1212316, 46.0688409))


    valid_3d = '''{
        "type": "LineString", 
        "coordinates": [
            [11.1212678, 46.0686443, 1],[11.1212316,46.0688409, 2]
        ]
    }'''

    pl_3d = to_polyline3d(valid_3d)
    assert pl_3d is not None
    assert type(pl_3d) == LineSegment3D
    assert pl_3d == LineSegment3D \
        .from_end_points(Point3D(11.1212678, 46.0686443, 1),
        Point3D(11.1212316,46.0688409, 2))
    
    valid_2d = '''{
        "type": "MultiLineString", 
        "coordinates": [
            [[10, 10], [20, 20], [10, 40]], 
            [[40, 40], [30, 30], [40, 20], [30, 10]]
        ]
    }'''

    pl_2d = to_polyline2d(valid_2d)
    assert pl_2d is not None
    assert type(pl_2d) == list
    assert pl_2d == [
        Polyline2D(vertices=[
                Point2D(10, 10),
                Point2D(20, 20),
                Point2D(10, 40)
                ]),
        Polyline2D(vertices=[
                Point2D(40, 40),
                Point2D(30, 30),
                Point2D(40, 20),
                Point2D(30, 10)
                ]),   
            ]

def test_geojson_to_polygon():
    valid_2d = '''{
        "type": "Polygon", 
        "coordinates": [
            [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]]
        ]
    }'''

    boundary = [
        Point2D(35, 10),
        Point2D(45, 45),
        Point2D(15, 40),
        Point2D(10, 20)
    ]

    vertices = [Point2D.from_array(_) for _ in boundary]

    pl_2d = to_polygon2d(valid_2d)
    assert pl_2d is not None
    assert type(pl_2d) == Polygon2D
    assert pl_2d == Polygon2D(vertices)

    valid_2d = '''{
        "type": "Polygon", 
        "coordinates": [
            [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]], 
            [[20, 30], [35, 35], [30, 20], [20, 30]]
        ]
    }'''

    holes = [[
        Point2D(20, 30),
        Point2D(35, 35),
        Point2D(30, 20)
    ]]

    pl_2d = to_polygon2d(valid_2d)
    assert pl_2d is not None
    assert type(pl_2d) == Polygon2D
    assert pl_2d == Polygon2D.from_shape_with_holes(boundary, holes)

def test_geojson_to_face():
    valid_2d = '''{
        "type": "Polygon", 
        "coordinates": [
            [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]]
        ]
    }'''

    boundary = [
        Point3D(35, 10, 0),
        Point3D(45, 45, 0),
        Point3D(15, 40, 0),
        Point3D(10, 20, 0)
    ]

    vertices = [Point3D.from_array(_) for _ in boundary]

    face = to_face3d(valid_2d)
    assert face is not None
    assert type(face) == Face3D
    assert face == Face3D(boundary=vertices)

    valid_2d = '''{
        "type": "Polygon", 
        "coordinates": [
            [[35, 10], [45, 45], [15, 40], [10, 20], [35, 10]], 
            [[20, 30], [35, 35], [30, 20], [20, 30]]
        ]
    }'''

    holes = [[
        Point3D(20, 30, 0),
        Point3D(35, 35, 0),
        Point3D(30, 20, 0)
    ]]

    face = to_face3d(valid_2d)
    assert face is not None
    assert type(face) == Face3D
    assert face == Face3D(boundary=boundary, 
        holes=holes)