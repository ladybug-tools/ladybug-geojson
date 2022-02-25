# coding=utf-8
'''Functions used as utility to convert Ladybug geometries from GEOJSON geometry strings.'''
from typing import List, Optional, Union

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

def _get_line_or_polyline_2d(arr: List[float],
    interpolated: Optional[bool]=False) -> \
    Union[LineSegment2D, Polyline2D]:
    if len(arr) == 2:
        return LineSegment2D.from_array(arr)
    
    pol = Polyline2D.from_array(arr)
    if interpolated:
        pol = Polyline2D(pol.vertices, interpolated)
    
    return pol