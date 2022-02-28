# coding=utf-8
''' Ladybug Feature class'''
import json
from typing import List, Optional
from ._validator import ( _Validator,
    GeojSONTypes )
from .convert.config import Options
from .convert.to_geometry import to_face3d, to_point3d, to_polyline3d
from ._geojson_helper import ( get_data_from_geojson_type,
    RFC7946 )

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
        * properties
    '''
    __slots__ = ('_geometry', 
        '_properties', '_options')

    def __init__(self, 
        json_string: str,
        options: Optional[Options]=Options.options_factory()):

        # preparation
        self._options = options
        # geometry set
        self._set_geometry(json_string)
        # property set
        self._set_properties(json_string)

    def _set_properties(self,
        json_string: str):
        prop, sel, err = get_data_from_geojson_type(json_string, 
            keyword=RFC7946.PROPERTIES,
            target=[GeojSONTypes.FEATURE],
            validation=False)
        
        if not sel:
            return err

        if not self._geometry:
            self._properties = None
            return err
        
        self._properties = prop

    def _set_geometry(self, 
        json_string: str):
        # preparation
        validation = self._options.get('validation')

        # validate here
        geo, sel, err = get_data_from_geojson_type(json_string, 
        keyword=RFC7946.GEOMETRY,
        target=[GeojSONTypes.FEATURE],
        validation=validation)
        
        if not sel:
            self._geometry = None
            return err
        
        # get json schema
        geo_schema = GeojSONTypes(geo.get('type'))

        # skip validation
        child_options = Options(validation=False)
        child_options.copy_from_dict(self._options.settings)

        geo = json.dumps(geo)
        if geo_schema in [GeojSONTypes.POINT, 
            GeojSONTypes.MULTIPOINT]:
            self._geometry = to_point3d(geo,
                child_options)
        elif geo_schema in [GeojSONTypes.LINESTRING, 
            GeojSONTypes.MULTILINESTRING]:
            self._geometry = to_polyline3d(geo,
                child_options)
        elif geo_schema in [GeojSONTypes.POLYGON, 
            GeojSONTypes.MULTIPOLYGON]:
            self._geometry = to_face3d(geo,
                child_options)

    @property
    def geometry(self):
        ''' Geometry. Ladybug geometry '''
        return self._geometry

    @property
    def properties(self):
        ''' Properties. Dictionary with all GeoJSON property '''
        return self._properties

    @classmethod
    def from_featurecollection(cls, 
        json_string: str,
        options: Optional[Options]=Options.options_factory()):
        # preparation
        validation = options.get('validation')

        # validate here
        features, sel, err = get_data_from_geojson_type(json_string, 
        keyword=RFC7946.FEATURES,
        target=[GeojSONTypes.FEATURE_COLLECTION],
        validation=validation)   

        if not sel:
            return err
        
        # skip validation
        child_options = Options(validation=False)
        child_options.copy_from_dict(options.settings)

        fts = []
        for ft in features:
            d = json.dumps(ft)
            fts.append(cls(d, child_options))
        
        return fts
