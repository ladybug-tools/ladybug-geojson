import json
from pathlib import Path
from typing import Optional
from .config import Options
from .._geojson_helper import ( RFC7946, 
    _run_validation  )
from .._validator import GeojSONTypes
from .to_geometry import ( to_collection_2d, 
    to_collection_3d, 
    to_face3d, 
    to_linesegment2d, 
    to_linesegment3d, 
    to_point2d, 
    to_point3d, 
    to_polygon2d )
from ..ladybug_feature import LadybugFeature

'''____________FROM GEOJSON DIRECTLY____________'''

def from_file(filepath: str,
    options: Optional[Options]=Options.options_factory(),
    is_3d: Optional[bool]=False):
    '''Function to convert geojson file into ladybug entities.
    
    Mapping for is_3d
    - POINT > Point3D 
    - MULTIPOINT > List[Point3D]
    - LINESTRING > LineSegment3D or Polyline3D
    - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
    - POLYGON > Face3D
    - MULTIPOLYGON > List[Face3D]
    - GEOMETRYCOLLECTION >
        - POINT > Point3D 
        - MULTIPOINT > List[Point3D]
        - LINESTRING > LineSegment3D or Polyline3D
        - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
        - POLYGON > Face3D
        - MULTIPOLYGON > List[Face3D]
    - FEATURE >
        - POINT > Point3D 
        - MULTIPOINT > List[Point3D]
        - LINESTRING > LineSegment3D or Polyline3D
        - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
        - POLYGON > Face3D
        - MULTIPOLYGON > List[Face3D]

    Mapping for not is_3d
    - POINT > Point2D 
    - MULTIPOINT > List[Point2D]
    - LINESTRING > LineSegment2D or Polyline2D
    - MULTILINESTRING > List[LineSegment2D] or List[Polyline2D]
    - POLYGON > Polygon2D or Face3D (on 2D space)
    - MULTIPOLYGON > List[Polygon2D] or List[Face3D]
    - GEOMETRYCOLLECTION >
        - POINT > Point2D 
        - MULTIPOINT > List[Point2D]
        - LINESTRING > LineSegment2D or Polyline2D
        - MULTILINESTRING > List[LineSegment2D] or List[Polyline2D]
        - POLYGON > Polygon2D or Face3D (on 2D space)
        - MULTIPOLYGON > List[Polygon2D] or List[Face3D] 
    - FEATURE >
        - POINT > Point3D 
        - MULTIPOINT > List[Point3D]
        - LINESTRING > LineSegment3D or Polyline3D
        - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
        - POLYGON > Face3D
        - MULTIPOLYGON > List[Face3D]

    Args:
    - json_string: GeoJSON string.
    - options: Options object to use for mapping.
    - is_3d: force to convert to 3d entities only.
            Note that LadybugFace has 3d geometry by default.

    Return:
        a ladybug geometry OR a list of ladybug geometry OR
        a LadybugFeature OR a list of LadybugFeature
    '''
    fp = Path(filepath)

    res = []
    if fp.exists():
        text = fp.read_text()
        res = from_geojson(json_string=text, 
            options=options, 
            is_3d=is_3d)
    return res


def from_geojson(json_string: str,
    options: Optional[Options]=Options.options_factory(),
    is_3d: Optional[bool]=False):
    '''Function to convert geojson into ladybug entities.
    
    Mapping for is_3d
    - POINT > Point3D 
    - MULTIPOINT > List[Point3D]
    - LINESTRING > LineSegment3D or Polyline3D
    - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
    - POLYGON > Face3D
    - MULTIPOLYGON > List[Face3D]
    - GEOMETRYCOLLECTION >
        - POINT > Point3D 
        - MULTIPOINT > List[Point3D]
        - LINESTRING > LineSegment3D or Polyline3D
        - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
        - POLYGON > Face3D
        - MULTIPOLYGON > List[Face3D]
    - FEATURE >
        - POINT > Point3D 
        - MULTIPOINT > List[Point3D]
        - LINESTRING > LineSegment3D or Polyline3D
        - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
        - POLYGON > Face3D
        - MULTIPOLYGON > List[Face3D]

    Mapping for not is_3d
    - POINT > Point2D 
    - MULTIPOINT > List[Point2D]
    - LINESTRING > LineSegment2D or Polyline2D
    - MULTILINESTRING > List[LineSegment2D] or List[Polyline2D]
    - POLYGON > Polygon2D or Face3D (on 2D space)
    - MULTIPOLYGON > List[Polygon2D] or List[Face3D]
    - GEOMETRYCOLLECTION >
        - POINT > Point2D 
        - MULTIPOINT > List[Point2D]
        - LINESTRING > LineSegment2D or Polyline2D
        - MULTILINESTRING > List[LineSegment2D] or List[Polyline2D]
        - POLYGON > Polygon2D or Face3D (on 2D space)
        - MULTIPOLYGON > List[Polygon2D] or List[Face3D] 
    - FEATURE >
        - POINT > Point3D 
        - MULTIPOINT > List[Point3D]
        - LINESTRING > LineSegment3D or Polyline3D
        - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
        - POLYGON > Face3D
        - MULTIPOLYGON > List[Face3D]

    Args:
    - json_string: GeoJSON string.
    - options: Options object to use for mapping.
    - is_3d: force to convert to 3d entities only.
        Note that LadybugFace has 3d geometry by default.

    Return:
        a ladybug geometry OR a list of ladybug geometry OR
        a LadybugFeature OR a list of LadybugFeature
    '''
    target = [
        GeojSONTypes.POINT,
        GeojSONTypes.MULTIPOINT,
        GeojSONTypes.LINESTRING,
        GeojSONTypes.MULTILINESTRING,
        GeojSONTypes.POLYGON,
        GeojSONTypes.MULTIPOLYGON,
        GeojSONTypes.FEATURE,
        GeojSONTypes.FEATURE_COLLECTION
    ]

    # validate all schema
    obj, sel, err = _run_validation(
        json_string=json_string,
        target=target
    )

    if err:
        return err
    
    # serialize
    item = json.dumps(obj)

    # skip validation for childs
    child_options = Options(validation=False)
    child_options.copy_from_dict(options.settings)

    # GoeJSON has oneOf so following is Ok
    if sel in [GeojSONTypes.FEATURE]:
        return LadybugFeature(json_string=item,
            options=child_options)
    elif sel in [GeojSONTypes.FEATURE_COLLECTION]:
        return LadybugFeature.from_featurecollection(
            json_string=item,
            options=child_options)

    if not is_3d:
        if sel in [GeojSONTypes.POINT,
            GeojSONTypes.MULTIPOINT]:
            return to_point2d(json_string=item,
                options=child_options)
        elif sel in [GeojSONTypes.LINESTRING,
            GeojSONTypes.MULTILINESTRING]:
            return to_linesegment2d(json_string=item,
                options=child_options)
        elif sel in [GeojSONTypes.POLYGON,
            GeojSONTypes.MULTIPOLYGON]:
            return to_polygon2d(json_string=item,
                options=child_options)
        elif sel in [GeojSONTypes.GEOMETRYCOLLECTION]:
            return to_collection_2d(json_string=item,
                options=child_options)
    else:
        if sel in [GeojSONTypes.POINT,
            GeojSONTypes.MULTIPOINT]:
            return to_point3d(json_string=item,
                options=child_options)
        elif sel in [GeojSONTypes.LINESTRING,
            GeojSONTypes.MULTILINESTRING]:
            return to_linesegment3d(json_string=item,
                options=child_options)
        elif sel in [GeojSONTypes.POLYGON,
            GeojSONTypes.MULTIPOLYGON]:
            return to_face3d(json_string=item,
                options=child_options)
        elif sel in [GeojSONTypes.GEOMETRYCOLLECTION]:
            return to_collection_3d(json_string=item,
                options=child_options)
