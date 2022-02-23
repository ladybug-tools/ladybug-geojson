'''Functions to create Ladybug geometries from GEOJSON geometry strings.'''
import json
from ._validator import ( _Validator,
    GeojSONTypes)
from typing import Optional, Union
try:
    from ladybug_geometry.geometry2d.pointvector import Vector2D, Point2D
    from ladybug_geometry.geometry2d.line import LineSegment2D
    from ladybug_geometry.geometry2d.polyline import Polyline2D
    from ladybug_geometry.geometry2d.polygon import Polygon2D
    from ladybug_geometry.geometry2d.mesh import Mesh2D
    from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
    from ladybug_geometry.geometry3d.line import LineSegment3D
    from ladybug_geometry.geometry3d.polyline import Polyline3D
    from ladybug_geometry.geometry3d.mesh import Mesh3D
    from ladybug_geometry.geometry3d.face import Face3D
    from ladybug_geometry.geometry3d.polyface import Polyface3D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

'''____________RFC 7946 KEYWORDS____________'''

COORDINATES = 'coordinates'

def _get_coordinates(json_string: str,
    target: str):
    validator = _Validator(json=json_string, 
        target=target)
    if not validator.is_valid:
        return

    obj = json.loads(json_string)
    arr = obj.get(COORDINATES)
    return arr

'''____________2D GEOMETRY TRANSLATORS____________'''

def to_vector2d(json_string: str) -> Vector2D:
    '''Ladybug Vector2D from GEOJSON Point.
        
    Args:
        json_string: GEOJSON geometry string to translate
    '''
    arr = _get_coordinates(json_string, 
        target=GeojSONTypes.POINT)
    if not arr:
        return

    return Vector2D.from_array(arr)

def to_point2d(json_string: str) -> Point2D:
    '''Ladybug Point2D from GEOJSON Point.
        
    Args:
        json_string: GEOJSON geometry string to translate
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.POINT)
    if not arr:
        return
    
    return Point2D.from_array(arr)

def to_linesegment2d(json_string: str) -> LineSegment2D:
    '''Ladybug LineSegment2D from GEOJSON LineString.
    
    Args:
        json_string: GEOJSON geometry string to translate
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.LINESTRING)
    if not arr:
        return

    if len(arr) > 2:
        arr =  arr[::len(arr)-1]

    return LineSegment2D.from_array(arr)


def to_polyline2d(json_string: str, 
    interpolated: Optional[bool]=False) -> Union[Polyline2D, LineSegment2D]:
    '''Ladybug Polyline2D from a GEOJSON LineString.
    A LineSegment2D will be returned if the input polyline has only two points.

    Args:
        json_string: GEOJSON geometry string to translate
        interpolated: set it to true to create smooth polylines
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.LINESTRING)
    if not arr:
        return

    if len(arr) == 2:
        return LineSegment2D.from_array(arr)

    pol = Polyline2D.from_array(arr)
    return pol if not interpolated else Polyline2D(pol.vertices, interpolated)

def to_polygon2d(json_string: str) -> Polygon2D:
    '''Ladybug Polygon2D from a GEOJSON Polygon.

    Args:
        json_string: GEOJSON geometry string to translate
    '''
    def to_pt(arr):
        return Point2D.from_array(arr)

    arr = _get_coordinates(json_string,
        target=GeojSONTypes.POLYGON)
    if not arr:
        return

    boundary = arr[0][:-1]

    if len(arr) == 1:
        return Polygon2D.from_array(boundary)
    
    boundary = list(map(to_pt, boundary))
    holes = [list(map(to_pt, 
        _[:-1])) for _ in arr[1:]]
    
    return Polygon2D.from_shape_with_holes(boundary, holes)

def to_mesh2d(json_string: str,
    missing_coordinate: Optional[float]=0.0) -> Mesh2D:
    '''Ladybug Mesh2D from a GEOJSON Polygon.

    Args:
        json_string: GEOJSON geometry string to translate
    '''
    face = to_face3d(json_string=json_string,
        missing_coordinate=missing_coordinate)
    
    if not face:
        return

    return face.triangulated_mesh2d

'''____________3D GEOMETRY TRANSLATORS____________'''

def to_vector3d(json_string: str) -> Vector3D:
    '''Ladybug Vector2D from GEOJSON Point.
        
    Args:
        json_string: GEOJSON geometry string to translate
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.POINT)
    if not arr:
        return
    
    return Vector3D.from_array(arr)

def to_point3d(json_string: str) -> Point3D:
    '''Ladybug Point2D from GEOJSON Point.
        
    Args:
        json_string: GEOJSON geometry string to translate
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.POINT)
    if not arr:
        return

    return Point3D.from_array(arr)


def to_linesegment3d(json_string: str) -> LineSegment3D:
    '''Ladybug LineSegment3D from GEOJSON LineString.
    
    Args:
        json_string: GEOJSON geometry string to translate
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.LINESTRING)
    if not arr:
        return

    if len(arr) > 2:
        arr =  arr[::len(arr)-1]

    return LineSegment3D.from_array(arr)


def to_polyline3d(json_string: str, 
    interpolated: Optional[bool]=False) -> Union[Polyline3D, LineSegment3D]:
    '''Ladybug Polyline3D from GEOJSON LineString.
    A LineSegment3D will be returned if the input polyline has only two points.

    Args:
        json_string: GEOJSON geometry string to translate
        interpolated: set it to true to create smooth polylines
    '''
    arr = _get_coordinates(json_string,
        target=GeojSONTypes.LINESTRING)
    if not arr:
        return

    if len(arr) == 2:
        return LineSegment3D.from_array(arr)

    pol = Polyline3D.from_array(arr)
    return pol if not interpolated else Polyline3D(pol.vertices, interpolated)

def to_face3d(json_string: str,
    missing_coordinate: Optional[float]=0.0) -> Face3D:
    '''Ladybug Face3D from a GEOJSON Polygon.

    Args:
        json_string: GEOJSON geometry string to translate
        missing_coordinate: it is used if z is missing.
    '''
    def to_pt(arr):
        out = arr[::]
        if len(arr) == 2:
            out.append(missing_coordinate)
        return Point3D.from_array(out)

    arr = _get_coordinates(json_string,
        target=GeojSONTypes.POLYGON)
    if not arr:
        return

    boundary = arr[0][:-1]
    boundary = list(map(to_pt, boundary))

    if len(arr) == 1:
        return Face3D(boundary=boundary)
    
    holes = [list(map(to_pt, 
        _[:-1])) for _ in arr[1:]]
    
    return Face3D(boundary=boundary, 
        holes=holes)