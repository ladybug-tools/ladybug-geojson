# coding=utf-8
import pytest

from ladybug_geojson.ladybug_feature import LadybugFeature

try:
    from ladybug_geometry.geometry3d.polyline import Polyline3D
    from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

def test_geojson_to_feature():
    valid_feature = '''
    {
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
        "name": "Via Rodolfo Belenzani",
        "array": [1, 2, 3, 4, 5] 
      }
    }
    '''
    feature = LadybugFeature(valid_feature)

    print(feature.properties)

    assert feature is not None
    assert type(feature) == LadybugFeature
    assert feature.geometry == Polyline3D(vertices=[
                Point3D(11.1214686,46.0677385),
                Point3D(11.121466,46.0677511),
                Point3D(11.1213806,46.0681452),
                Point3D(11.1213548,46.0682642),
                Point3D(11.1213115,46.0684385),
                Point3D(11.1212897,46.0685261),
                Point3D(11.1212678,46.0686443)
                ])
    assert feature.properties == {
        'lanes': 1,
        'name': 'Via Rodolfo Belenzani',
        'array': [1,2,3,4,5]
    }

