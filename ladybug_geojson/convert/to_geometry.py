# coding=utf-8
'''Functions to create Ladybug geometries from GEOJSON geometry strings.'''
import json
from .._validator import GeojSONTypes
from .._geometry_helper import ( _add_z_coordinate, 
    _get_line_2d,
    _get_line_3d, 
    _get_line_or_polyline_2d,
    _get_line_or_polyline_3d,
    _to_polygon_2d, _to_face )
from .._geojson_helper import ( get_data_from_geojson_type,
    RFC7946)
from .config import Options
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


'''____________COLLECTION GEOMETRY TRANSLATORS____________'''

def to_collection_2d(json_string: str, 
    options: Optional[Options]=Options.options_factory()):
    '''Ladybug Geometry 2D from GEOJSON GeometryCollection.
    Mapping is
    - POINT > Point2D 
    - MULTIPOINT > List[Point2D]
    - LINESTRING > LineSegment2D or Polyline2D
    - MULTILINESTRING > List[LineSegment2D] or List[Polyline2D]
    - POLYGON > Polygon2D or Face3D (on 2D space)
    - MULTIPOLYGON > List[Polygon2D] or List[Face3D]
    
    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.GEOMETRYCOLLECTION]
    validation = options.get('validation')
    fill_polygon = options.get('fill_polygon')

    arr, sel, err = get_data_from_geojson_type(json_string, 
        keyword=RFC7946.GEOMETRY_COLLECTION,
        target=mapping,
        validation=validation)
    if not arr:
        return err
    
    res = []

    # skip validation for childs
    child_options = Options(validation=False)
    child_options.copy_from_dict(options.settings)

    for item in arr:
        if item.get('type') == GeojSONTypes.POINT.value:
            item = json.dumps(item)
            res.append(to_point2d(item, child_options))
        elif item.get('type') == GeojSONTypes.MULTIPOINT.value:
            item = json.dumps(item)
            res.extend(to_point2d(item, child_options))
        elif item.get('type') == GeojSONTypes.LINESTRING.value:
            item = json.dumps(item)
            res.append(to_polyline2d(item, child_options))
        elif item.get('type') == GeojSONTypes.MULTILINESTRING.value:
            item = json.dumps(item)
            res.extend(to_polyline2d(item, child_options))
        elif item.get('type') == GeojSONTypes.POLYGON.value:
            item = json.dumps(item)
            if fill_polygon:
                res.append(to_face3d(item, child_options))
            else:
                res.append(to_polygon2d(item, options))
        elif item.get('type') == GeojSONTypes.MULTIPOLYGON.value:
            item = json.dumps(item)
            if fill_polygon:
                res.extend(to_face3d(item, child_options))
            else:
                res.extend(to_polygon2d(item, child_options))

    return res

def to_collection_3d(json_string: str, 
    options: Optional[Options]=Options.options_factory()):
    '''Ladybug Geometry 3D from GEOJSON GeometryCollection.
    Mapping is
    - POINT > Point3D 
    - MULTIPOINT > List[Point3D]
    - LINESTRING > LineSegment3D or Polyline3D
    - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
    - POLYGON > Face3D
    - MULTIPOLYGON > List[Face3D]
    
    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.GEOMETRYCOLLECTION]
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string, 
        keyword=RFC7946.GEOMETRY_COLLECTION,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    # skip validation for childs
    child_options = Options(validation=False)
    child_options.copy_from_dict(options.settings)
    
    res = []
    for item in arr:
        if item.get('type') == GeojSONTypes.POINT.value:
            item = json.dumps(item)
            res.append(to_point3d(item, child_options))
        elif item.get('type') == GeojSONTypes.MULTIPOINT.value:
            item = json.dumps(item)
            res.extend(to_point3d(item, child_options))
        elif item.get('type') == GeojSONTypes.LINESTRING.value:
            item = json.dumps(item)
            res.append(to_polyline3d(item, child_options))
        elif item.get('type') == GeojSONTypes.MULTILINESTRING.value:
            item = json.dumps(item)
            res.extend(to_polyline3d(item, child_options))
        elif item.get('type') == GeojSONTypes.POLYGON.value:
            item = json.dumps(item)
            res.append(to_face3d(item, child_options))
        elif item.get('type') == GeojSONTypes.MULTIPOLYGON.value:
            item = json.dumps(item)
            res.extend(to_face3d(item, child_options))

    return res

'''____________2D GEOMETRY TRANSLATORS____________'''

def to_vector2d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[Vector2D, List[Vector2D]]:
    '''Ladybug Vector2D from GEOJSON Point or Multipoint.
        
    Args:
    - json_string: GEOJSON geometry string to translate
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.POINT, GeojSONTypes.MULTIPOINT]
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string, 
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.POINT:
        return Vector2D.from_array(arr)
    else:
        return [Vector2D.from_array(_) for _ in arr]


def to_point2d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[Point2D, List[Point2D]]:
    '''Ladybug Point2D from GEOJSON Point or Multipoint.
        
    Args:
    - json_string: GEOJSON geometry string to translate
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.POINT, GeojSONTypes.MULTIPOINT]
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.POINT:
        return Point2D.from_array(arr)
    else:
        return [Point2D.from_array(_) for _ in arr]


def to_linesegment2d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[LineSegment2D, List[LineSegment2D]]:
    '''Ladybug LineSegment2D from GEOJSON LineString or MultiLineString.
    
    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.LINESTRING,
            GeojSONTypes.MULTILINESTRING]
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.LINESTRING:
        return _get_line_2d(arr)
    else:
        return list(map(_get_line_2d, arr))


def to_polyline2d(json_string: str, 
    options: Optional[Options]=Options.options_factory()) -> \
        Union[Polyline2D, LineSegment2D,
        List[Polyline2D], List[LineSegment2D]]:
    '''Ladybug Polyline2D from a GEOJSON LineString or MultiLineString.
    A LineSegment2D will be returned if the input polyline has only 
    two points and it is a LineString.

    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.LINESTRING,
            GeojSONTypes.MULTILINESTRING]
    validation = options.get('validation')
    interpolated = options.get('interpolated')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.LINESTRING:
        return _get_line_or_polyline_2d(arr, 
            interpolated=interpolated)
    else:
        return list(map(lambda _: _get_line_or_polyline_2d(_, 
            interpolated=interpolated), arr))


def to_polygon2d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[Polygon2D, List[Polygon2D]]:
    '''Ladybug Polygon2D from a GEOJSON Polygon.

    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.POLYGON, 
            GeojSONTypes.MULTIPOLYGON]
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.POLYGON:
        return _to_polygon_2d(arr)
    else:
        return list(map(_to_polygon_2d, arr))
    

def to_mesh2d(json_string: str,
    options: Optional[Options]=Options.options_factory()) -> \
        Union[Mesh2D, List[Mesh2D]]:
    '''Ladybug Mesh2D from a GEOJSON Polygon or MultiPolygon.

    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    face = to_face3d(json_string=json_string,
        options=options)
    
    if not face:
        return 'Validation err'
    
    if type(face) == list:
        return [_.triangulated_mesh2d for _ in face]
    
    return face.triangulated_mesh2d

'''____________3D GEOMETRY TRANSLATORS____________'''

def to_vector3d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[Vector3D, List[Vector3D]]:
    '''Ladybug Vector2D from GEOJSON Point or MultiPoint.
        
    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.POINT, GeojSONTypes.MULTIPOINT]
    z = options.get('z')
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err
    
    if sel == GeojSONTypes.POINT:
        return Vector3D.from_array(_add_z_coordinate(arr, 
            z))
    else:
        return list(map(lambda _: Vector3D.from_array(
            _add_z_coordinate(_, 
            z), 
        arr)))


def to_point3d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[Point3D, List[Point3D]]:
    '''Ladybug Point2D from GEOJSON Point or MultiPoint.
        
    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.POINT, GeojSONTypes.MULTIPOINT]
    z = options.get('z')
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.POINT:
        return Point3D.from_array(_add_z_coordinate(arr, 
            z))
    else:
        return list(map(lambda _: Point3D.from_array(
            _add_z_coordinate(_, 
            z), 
        arr)))


def to_linesegment3d(json_string: str,
        options: Optional[Options]=Options.options_factory()) -> \
        Union[LineSegment3D, List[LineSegment3D]]:
    '''Ladybug LineSegment3D from GEOJSON LineString or MultiLineString.
    
    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''    
    # preparation
    mapping = [GeojSONTypes.LINESTRING, 
            GeojSONTypes.MULTILINESTRING]
    z = options.get('z')
    validation = options.get('validation')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.LINESTRING:
        return _get_line_3d(arr, z)
    else:
        return list(map(lambda _: 
            _get_line_3d(_, z), arr))


def to_polyline3d(json_string: str, 
    options: Optional[Options]=Options.options_factory()) -> \
        Union[Polyline3D, LineSegment3D,
        List[Polyline3D], List[LineSegment3D]]:
    '''Ladybug Polyline3D from GEOJSON LineString.
    A LineSegment3D will be returned if the input polyline has only two points.

    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.LINESTRING, 
            GeojSONTypes.MULTILINESTRING]
    validation = options.get('validation')
    interpolated = options.get('interpolated')
    z = options.get('z')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.LINESTRING:
        return _get_line_or_polyline_3d(arr, 
            interpolated=interpolated, 
            z=z)
    else:
        return list(map(lambda _ : _get_line_or_polyline_3d(
            _, interpolated=interpolated, 
            z=z
        ), 
        arr))


def to_face3d(json_string: str,
    options: Optional[Options]=Options.options_factory()) -> \
        Union[Face3D, List[Face3D]]:
    '''Ladybug Face3D or Polyface3D from a GEOJSON Polygon or MultiPolygon.

    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    # preparation
    mapping = [GeojSONTypes.POLYGON, 
            GeojSONTypes.MULTIPOLYGON]
    validation = options.get('validation')
    merge_faces = options.get('merge_faces')
    tolerance = options.get('tolerance')
    z = options.get('z')

    arr, sel, err = get_data_from_geojson_type(json_string,
        keyword=RFC7946.COORDINATES,
        target=mapping,
        validation=validation)
    if not arr:
        return err

    if sel == GeojSONTypes.POLYGON:
        return _to_face(arr, z)
    
    faces = list(map(lambda _: 
        _to_face(_, z), 
        arr))

    # try merge
    if merge_faces:
        try:
            faces = Polyface3D.from_faces(faces, tolerance)
        except:
            pass
    return faces
    

def to_mesh3d(json_string: str,
    options: Optional[Options]=Options.options_factory()) -> Mesh2D:
    '''Ladybug Mesh3D from a GEOJSON Polygon or MultiPolygon.

    Args:
    - json_string: GEOJSON geometry string to translate.
    - options: Options object to use for mapping.
    '''
    face = to_face3d(json_string=json_string,
        options=options)
    
    if not face:
        return 'Validation err'
    
    if type(face) == list:
        return [_.triangulated_mesh3d for _ in face]
    
    return face.triangulated_mesh3d
