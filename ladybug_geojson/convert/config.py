# coding=utf-8
'''Options for geojson convert.'''
from typing import Any

class Options:
    '''Option for the mapping. Only some fields will be used.
        It depends on geometry type.

    Args:
    - z: valid Feature JSON string.
    - interpolated: set it to true to create smooth polylines.
    - merge_faces: try to create polyface from list of faces, only if MultiPolygon.
    - validation: set it to false to skip GeoJSON validation.
    - fill_polygon: set it to true to create faces instead of polygon.
    - tolerance: number to use as tolerance for the polyface operatation.
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
        ''' Create a default Options object '''
        return cls()

    def get(self, 
        keyword: str):
        ''' Get value from settings '''
        return self._settings.get(keyword)
    
    def set(self, 
        keyword: str,
        value: Any):
        ''' Set value into settings '''
        self._settings[keyword] = value
    
    def copy_from_dict(self, 
        other:dict):
        ''' Merge current settings with another dictionary '''
        self._settings = {**other, **self._settings}
    
    @property
    def settings(self):
        ''' Get dict options to use with convert '''
        return self._settings
