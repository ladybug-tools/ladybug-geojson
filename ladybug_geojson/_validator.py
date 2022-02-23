# coding=utf-8
import json
from pathlib import Path
from argparse import ArgumentError
from jsonschema import ( validate, 
    ValidationError, 
    SchemaError )

'''Class for geojson validation.'''
class _Validator:

    SCHEMA_PATH = './schema'
    VALID_GEO_TYPES = (
        'Point', 
        'LineString', 
        'Polygon', 
        'MultiPoint', 
        'MultiLineString', 
        'MultiPolygon',
        'GeometryCollection'
    )
    
    '''Class for geojson validation.
    Args:
        json: input JSON string 
    Properties:
        * is_valid
    '''
    __slots__ = ('_json')

    def __init__(self, 
        json: str):
        self._json = json

    @property
    def is_valid(self):
        ''' JSON string is valid '''
        return self._validation()
    
    def _validation(self):
        # get geojson type
        obj = json.loads(self._json)
        
        # type key not found
        tp = obj.get('type')
        if not tp:
            return

        if tp not in self.VALID_GEO_TYPES:
                 raise ArgumentError(message=f'{type} is' + 
                 'not a valid key.')

        # get geojson schema
        valid_schema = json.loads(self._read_schema(tp))
        
        try:
            if tp == 'Point':
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

    def _read_schema(self, 
        type: str):
        ''' Read geojson schema '''
        env_path = Path(__file__).parent

        schema_name = type.lower() + '.json'
        schema = env_path.joinpath(self.SCHEMA_PATH, schema_name)
        text = schema.read_text()
        return text
