# coding=utf-8
import json
from enum import ( Enum, unique )
from pathlib import Path
from typing import List
from jsonschema import ( validate, 
    ValidationError, 
    SchemaError )

@unique
class GeojSONTypes(Enum):
    POINT = 'Point'
    LINESTRING = 'LineString'
    POLYGON = 'Polygon'
    MULTIPOINT = 'MultiPoint'
    MULTILINESTRING = 'MultiLineString'
    MULTIPOLYGON = 'MultiPolygon'
    GEOMETRYCOLLECTION = 'GeometryCollection'
    FEATURE = 'Feature'
    FEATURE_COLLECTION = 'FeatureCollection'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

'''Class for geojson validation.'''
class _Validator:
    SCHEMA_PATH = './schema'
    
    '''Class for geojson validation.
    Args:
    - json: input JSON string 
    - target: list of GeojSONTypes used for validation
    '''
    __slots__ = ('_selection',
        '_error')

    def __init__(self, 
        json: str,
        target: List[GeojSONTypes]):

        self._selection = self._validation(json, 
            target)

    @property
    def selection(self):
        ''' Schema used '''
        return self._selection

    @property
    def error(self):
        ''' Error '''
        return self._error

    def _validation(self, 
        data: str, 
        target: List[GeojSONTypes]):
        # get geojson type
        obj = json.loads(data)
        self._error = None
        
        # type key not found
        tp = obj.get('type')
        if not tp:
            return
        
        # skip if it is not the target
        target_values = [_.value for _ in target]
        if tp not in target_values:
            return

        if not GeojSONTypes.has_value(tp):
            raise Exception(f'{tp} is' + 
            'not a valid key.')

        # get geojson schema
        valid_schema = json.loads(self._read_schema(tp))
        
        try:
            validate(instance=obj, 
                schema=valid_schema)
            
        except SchemaError as e:
            self._error = f'Geojson schema is not valid: {e}'
            return

        except ValidationError as e:
            self._error = f'Geojson is not valid: {e}'
            return

        except Exception as e:
            self._error = e
            return
        
        return GeojSONTypes(tp)

    def _read_schema(self,
        type: str):
        ''' Read geojson schema '''
        env_path = Path(__file__).parent
        schema_name = type.lower() + '.json'
        schema = env_path.joinpath(self.SCHEMA_PATH, schema_name)
        text = schema.read_text()
        return text
