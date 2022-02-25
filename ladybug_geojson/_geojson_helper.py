# coding=utf-8
'''Functions used as utility to convert GEOJSON strings.'''
import json
from enum import ( Enum, unique )
from ._validator import ( _Validator,
    GeojSONTypes)
from typing import List, Optional, Union

'''____________RFC 7946 KEYWORDS____________'''

@unique
class RFC7946(Enum):
    COORDINATES = 'coordinates'
    GEOMETRY_COLLECTION = 'geometries'
    PROPERTIES = 'properties'
    GEOMETRY = 'geometry'

def _get_data_from_json(json_string: str,
    keyword: RFC7946,
    target: List[GeojSONTypes],
    validation: Optional[bool]=False):

    sel = None
    # complete validation with GeoJSON schema
    if not validation:
        validator = _Validator(json=json_string, 
            target=target)
        if not validator.selection:
            return None, None
        sel = validator.selection

    obj = json.loads(json_string)

    # get just the type as fast validation
    if validation:
        try:
            sel = GeojSONTypes(obj.get('type'))
        except:
            return None, None

    arr = obj.get(keyword.value)
    return arr, sel


class Options:
    '''Option for the mapping. Only some fields will be used.
        It depends on geometry type.

    Args:
        z: valid Feature JSON string.
        interpolation: set it to true to create smooth polylines.
        merge_faces: try to create polyface from list of faces, only if MultiPolygon.
        validation: set it to true to skip GeoJSON validation.
        tolerance: number to use as tolerance for the polyface operatation.
    Properties:
        * settings
    '''
    __slots__ = ('_settings')

    def __init__(self,
        z: Optional[float]=0.0, 
        interpolation: Optional[bool]=False, 
        merge_faces: Optional[bool]=False,
        validation: Optional[bool]=False,
        tolerance: Optional[bool]=0.001):
        self._settings = {
            'z': z,
            'merge_faces': merge_faces,
            'interolation': interpolation,
            'validation': validation,
            'tolernace': tolerance
        }
    
    @classmethod
    def options_factory(cls):
        return cls()

    @property
    def settings(self):
        return self._settings