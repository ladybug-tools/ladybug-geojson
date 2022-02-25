# coding=utf-8
'''Functions used as utility to convert GEOJSON strings.'''
import json
from enum import ( Enum, unique )
from ._validator import ( _Validator,
    GeojSONTypes)
from typing import Any, List, Optional, Union

'''____________RFC 7946 KEYWORDS____________'''

@unique
class RFC7946(Enum):
    COORDINATES = 'coordinates'
    GEOMETRY_COLLECTION = 'geometries'
    PROPERTIES = 'properties'
    GEOMETRY = 'geometry'
    TYPE = 'type'
    FEATURES = 'features'

def _get_data_from_json(json_string: str,
    keyword: RFC7946,
    target: List[GeojSONTypes],
    validation: Optional[bool]=True,
    shallow_validation: Optional[RFC7946]=RFC7946.TYPE):
    '''Function to validate data and extract data by keyword.
    
    Args:
        json_string: JSON string to use for validation and query.
        keyword: RFC7946 keyword to use for data query (data to extract).
        target: list of schema used for validation.
        validation: enable or disable the validation. If disabled it check 
            using shallow_validation
        shallow_validation: fast validation using just a keyword.
            if TYPE it returns GeojSONTypes
            if PROPERTIES it returns property keyword itself
    '''

    sel = None
    # complete and slow validation with GeoJSON schema
    if validation:
        validator = _Validator(json=json_string, 
            target=target)
        if not validator.selection:
            return None, None
        sel = validator.selection

    obj = json.loads(json_string)

    # fast validation
    if not validation:
        if shallow_validation == RFC7946.TYPE:
            sel = GeojSONTypes(obj.get(RFC7946.TYPE.value))
        elif shallow_validation == RFC7946.PROPERTIES:
            sel = RFC7946.PROPERTIES
        else:
            return None, None

    arr = obj.get(keyword.value)
    return arr, sel


class Options:
    '''Option for the mapping. Only some fields will be used.
        It depends on geometry type.

    Args:
        z: valid Feature JSON string.
        interpolated: set it to true to create smooth polylines.
        merge_faces: try to create polyface from list of faces, only if MultiPolygon.
        validation: set it to false to skip GeoJSON validation.
        fill_polygon: set it to true to create faces instead of polygon.
        tolerance: number to use as tolerance for the polyface operatation.
    Properties:
        * settings
    '''
    __slots__ = ('_settings')

    def __init__(self,
        z: float=0.0, 
        interpolated: bool=False, 
        merge_faces: bool=False,
        validation: bool=True,
        fill_polygon: bool=False,
        tolerance: bool=0.001):
        self._settings = {
            'z': z,
            'merge_faces': merge_faces,
            'interpolated': interpolated,
            'validation': validation,
            'fill_polygon': fill_polygon,
            'tolerance': tolerance
        }
    
    @classmethod
    def options_factory(cls):
        return cls()

    def get(self, 
        keyword: str):
        return self._settings.get(keyword)
    
    def set(self, 
        keyword: str,
        value: Any):
        self._settings[keyword] = value
    
    def copy_from_dict(self, 
        other:dict):
        self._settings = {**other, **self._settings}
    
    @property
    def settings(self):
        return self._settings