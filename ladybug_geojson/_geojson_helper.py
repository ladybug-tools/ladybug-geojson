# coding=utf-8
'''Functions used as utility to convert GEOJSON strings.'''
import json
from enum import ( Enum, unique )
from ._validator import ( _Validator,
    GeojSONTypes)
from typing import Any, List, Optional, Union
from .convert.config import Options

'''____________RFC 7946 KEYWORDS____________'''

@unique
class RFC7946(Enum):
    ''' Keyword used for query '''
    COORDINATES = 'coordinates'
    GEOMETRY_COLLECTION = 'geometries'
    PROPERTIES = 'properties'
    GEOMETRY = 'geometry'
    TYPE = 'type'
    FEATURES = 'features'


def get_data_from_geojson_type(json_string: str,
    keyword: RFC7946,
    target: List[GeojSONTypes],
    validation: Optional[bool]=True):
    '''Function to validate data and extract data by keyword.
    
    Args:
    - json_string: JSON string to use for validation and query.
    - keyword: RFC7946 keyword to use for data query (data to extract).
    - target: list of schema used for validation.
    - validation: enable or disable the validation using Geojson Schema. 
            If it is disabled a fast validation will be used - 
            just the TYPE keyword it returns GeojSONTypes

    Return:
        a tuple with 3 items (objects, schema used, error 
            message if validation error)
    '''

    obj, sel, err = _run_validation(
        json_string=json_string,
        target=target,
        validation=validation
    )
    
    if not sel:
        return None, None, err

    arr = obj.get(keyword.value)
    return arr, sel, None


'''____________PRIVATE VALIDATION FUNCTION____________'''

def _run_validation(json_string: str,
    target: List[GeojSONTypes],
    validation: Optional[bool]=True):
    '''Function to validate data and extract data by keyword.
    
    Args:
    - json_string: JSON string to use for validation and query.
    - keyword: RFC7946 keyword to use for data query (data to extract).
    - target: list of schema used for validation.
    - validation: enable or disable the validation using Geojson Schema. 
            If it is disabled a fast validation will be used - 
            just the TYPE keyword it returns GeojSONTypes

    Return:
        a tuple with 3 items (objects, schema used, error 
            message if validation error)
    '''

    sel = None # schema used
    # complete and slow validation with GeoJSON schema
    if validation:
        validator = _Validator(json=json_string, 
            target=target)
        if not validator.selection:
            return None, None, validator.error
        sel = validator.selection

    obj = json.loads(json_string)

    # fast validation
    if not validation:
        tp = obj.get(RFC7946.TYPE.value)
        if tp:
            sel = GeojSONTypes(tp)
        else:
            return None, None, 'Geojson type not found.'

    return obj, sel, None