'''Functions to create Ladybug geometries from GEOJSON strings.'''
import json
from ._validator import _Validator
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

'''____________2D GEOMETRY TRANSLATORS____________'''

def to_vector2d(json_string: str) -> Vector2D:
    '''Ladybug Vector2D from GEOJSON Point.'''
    validator = _Validator(json_string)
    if not validator.is_valid:
        return

    obj = json.loads(json_string)
    arr = obj.get('coordinates')
    return Vector2D.from_array(arr)