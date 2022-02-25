# coding=utf-8
''' Ladybug Feature class'''
from pickle import LIST
from tkinter.tix import Tree
from typing import Optional
from ._validator import ( _Validator,
    GeojSONTypes )
from .geojson_helper import ( _get_data_from_json,
    RFC7946, Options )
from .to_geometry import ( to_face3d, to_point3d, to_polyline3d )

class LadybugFeature:
    '''Ladybug feature

    Mapping for geometry
    - POINT > Point3D 
    - MULTIPOINT > List[Point3D]
    - LINESTRING > LineSegment3D or Polyline3D
    - MULTILINESTRING > List[LineSegment3D] or List[Polyline3D]
    - POLYGON > Face3D
    - MULTIPOLYGON > List[Face3D]

    Args:
        json_string: valid Feature JSON string.
        settings: Settings type to use for options.
        validation: set it to true to skip GeoJSON validation.
    Properties:
        * geometry
        * property
    '''
    __slots__ = ('_geometry', 
        '_property')

    def __init__(self, 
        json_string: str,
        options: Optional[Options]=Options.options_factory):

        # preparation
        self._options = options
        mapping = [GeojSONTypes.FEATURE]

        # geometry set
        validation = self._options.get('validation')
        self._init_geometry(json_string, 
            validation, 
            mapping)

        # property set - skip validation
        prop, schema_used = _get_data_from_json(json_string, 
            keyword=RFC7946.PROPERTIES,
            target=mapping,
            validation=True)

    def _init_geometry(self, 
        json_string: str, 
        validation: bool, 
        mapping: LIST[GeojSONTypes]):

        # validate just one
        geo, geo_schema = _get_data_from_json(json_string, 
        keyword=RFC7946.GEOMETRY,
        target=mapping,
        validation=validation)
        
        if not geo_schema:
            return

        # preparation

        
        if geo_schema in [GeojSONTypes.POINT, 
            GeojSONTypes.MULTIPOINT]:
            self._geometry = to_point3d(geo,
                validation=True)
        elif geo_schema in [GeojSONTypes.LINESTRING, 
            GeojSONTypes.MULTILINESTRING]:
            self._geometry = to_polyline3d(geo,
                validation=True)
        elif geo_schema in [GeojSONTypes.POLYGON, 
            GeojSONTypes.MULTIPOLYGON]:
            self._geometry = to_face3d(geo,
                validation=True)

    @property
    def geometry(self):
        ''' Geometry '''
        return self._geometry
