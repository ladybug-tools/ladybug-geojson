# coding=utf-8
import pytest
from ladybug_geojson.convert.geojson import ( from_geojson,
    from_file )
from pathlib import Path
from ladybug_geojson.convert.config import Options

try:
    # from ladybug_geometry.geometry2d.pointvector import Vector2D, Point2D
    # from ladybug_geometry.geometry2d.line import LineSegment2D
    # from ladybug_geometry.geometry2d.polyline import Polyline2D
    # from ladybug_geometry.geometry2d.polygon import Polygon2D
    # from ladybug_geometry.geometry2d.mesh import Mesh2D
    from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
    # from ladybug_geometry.geometry3d.line import LineSegment3D
    from ladybug_geometry.geometry3d.polyline import Polyline3D
    # from ladybug_geometry.geometry3d.mesh import Mesh3D
    from ladybug_geometry.geometry3d.face import Face3D
    # from ladybug_geometry.geometry3d.polyface import Polyface3D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

def test_geojson_to_feature():
    
    geojson = '''
    { "type": "FeatureCollection",
    "features": [
        { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
        "properties": {"prop0": "value0"}
        },
        { "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
            [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
            ]
            },
        "properties": {
            "prop0": "value0",
            "prop1": 0.0
            }
        },
        { "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
            [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                [100.0, 1.0], [100.0, 0.0] ]
            ]

        },
        "properties": {
            "prop0": "value0",
            "prop1": {"this": "that"}
            }
        }
        ]
    }
    '''

    boundary = [
        Point3D(100, 0),
        Point3D(101, 0),
        Point3D(101, 1),
        Point3D(100, 1)
    ]

    vertices = [Point3D.from_array(_) for _ in boundary]

    objs = from_geojson(geojson) 
    assert objs[0].geometry.x == 102.0
    assert objs[0].properties == {"prop0": "value0"}
    assert len(objs) == 3
    assert objs[2].geometry == Face3D(boundary=vertices)
    assert type(objs[1].geometry) is Polyline3D 


def test_from_file():
    fp = './files/molise.json'
    env_path = Path(__file__).parent
    full_path = env_path.joinpath(fp)

    objs = from_file(full_path)
    print(len(objs))
    assert type(objs[0].geometry) == Face3D
    assert objs[30].properties['name'] == 'Larino'