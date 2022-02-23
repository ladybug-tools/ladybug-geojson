# coding=utf-8
import json
from enum import ( Enum, unique )
from pathlib import Path
from argparse import ArgumentError
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

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

'''Class for geojson validation.'''
class _Validator:
    SCHEMA_PATH = './schema'
    
    '''Class for geojson validation.
    Args:
        json: input JSON string 
    Properties:
        * is_valid
    '''
    __slots__ = ('_json', '_target')

    def __init__(self, 
        json: str,
        target: GeojSONTypes):
        self._json = json
        self._target = target

    @property
    def is_valid(self):
        ''' JSON string is valid '''
        return self._validation()
    
    @property
    def target(self):
        ''' JSON type target '''
        return self._target
    
    def _validation(self):
        # get geojson type
        obj = json.loads(self._json)
        
        # type key not found
        tp = obj.get('type')
        if not tp:
            return

        # skip if it is not the target
        if self._target.value != tp:
            return

        if not GeojSONTypes.has_value(tp):
            raise Exception(f'{tp} is' + 
            'not a valid key.')

        # get geojson schema
        valid_schema = json.loads(self._read_schema())
        
        try:
            validate(instance=obj, 
                schema=valid_schema)
            
        except SchemaError as e:
            print(f'Geojson schema is not valid: {e}')
            return

        except ValidationError as e:
            print(f'Geojson is not valid: {e}')
            return

        except Exception as e:
            print(e)
            return
        
        return True

    def _read_schema(self):
        ''' Read geojson schema '''
        env_path = Path(__file__).parent
        schema_name = self._target.value.lower() + '.json'
        schema = env_path.joinpath(self.SCHEMA_PATH, schema_name)
        text = schema.read_text()
        return text
