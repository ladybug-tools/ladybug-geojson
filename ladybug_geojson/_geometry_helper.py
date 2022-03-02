# coding=utf-8
'''Functions used as utility to convert Ladybug geometries from GEOJSON geometry strings.'''
from typing import List, Optional, Union

try:
    from ladybug_geometry.geometry2d.pointvector import Point2D
    from ladybug_geometry.geometry3d.plane import Plane
    from ladybug_geometry.geometry2d.line import LineSegment2D
    from ladybug_geometry.geometry2d.polyline import Polyline2D
    from ladybug_geometry.geometry2d.polygon import Polygon2D
    from ladybug_geometry.geometry3d.pointvector import Point3D
    from ladybug_geometry.geometry3d.line import LineSegment3D
    from ladybug_geometry.geometry3d.polyline import Polyline3D
    from ladybug_geometry.geometry3d.face import Face3D
except ImportError as e:
    raise ImportError(
        f'Failed to import ladybug_geometry.\n{e}')

def _add_z_coordinate(arr: List[float], 
    z: float) -> List[float]:
    out = arr[::]
    if len(arr) == 2:
        out.append(z)
    return out

def _get_line_2d(arr: List[float]) -> LineSegment2D:
    res = arr
    if len(arr) > 2:
        res = arr[::len(arr)-1]
    return LineSegment2D.from_array(res)

def _get_line_3d(arr: List[float],
    z: Optional[float]=0.0)-> LineSegment3D:
    res = arr
    if len(arr) > 2:
        res = arr[::len(arr)-1]
    
    # [[],[]]
    res = list(map(lambda _: 
        _add_z_coordinate(_, z), res))

    return LineSegment3D.from_array(res)

def _get_line_or_polyline_3d(arr: List[float],
    interpolated: Optional[bool]=False,
    z: Optional[float]=0.0) -> \
    Union[LineSegment3D, Polyline3D]:
    arr = list(map(lambda _: _add_z_coordinate(_, z), 
        arr))
    if len(arr) == 2:
        return LineSegment3D.from_array(arr)
    
    pol = Polyline3D.from_array(arr)
    if interpolated:
        pol = Polyline3D(pol.vertices, interpolated)
    
    return pol

def _get_line_or_polyline_2d(arr: List[float],
    interpolated: Optional[bool]=False) -> \
    Union[LineSegment2D, Polyline2D]:
    if len(arr) == 2:
        return LineSegment2D.from_array(arr)
    
    pol = Polyline2D.from_array(arr)
    if interpolated:
        pol = Polyline2D(pol.vertices, interpolated)
    
    return pol

def _to_polygon_2d(arr: List[float]) -> Polygon2D:
    boundary = arr[0][:-1]
    if len(arr) == 1:
        return Polygon2D.from_array(boundary)
    
    boundary = list(map(Point2D.from_array, boundary))
    holes = [list(map(Point2D.from_array, 
        _[:-1])) for _ in arr[1:]]
    return Polygon2D.from_shape_with_holes(boundary, 
        holes)

def _to_face(arr: List[float], 
    z: float):
    boundary = arr[0][:-1]
    boundary = list(map(lambda _: 
        Point3D.from_array(_add_z_coordinate(_, z)), 
        boundary))

    # I suppose it is on XY plane
    pt = boundary[0]
    plane = Plane(o=pt)

    if len(arr) == 1:
        return Face3D(boundary=boundary, 
            plane=plane)
    
    holes = [list(map(lambda l: 
        Point3D.from_array(_add_z_coordinate(l, z)), 
        _[:-1])) for _ in arr[1:]]
    
    return Face3D(boundary=boundary, 
        holes=holes,
        plane=plane)