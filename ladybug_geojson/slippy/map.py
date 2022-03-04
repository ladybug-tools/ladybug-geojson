# coding=utf-8
'''Util to get skippy map tilenames.'''
import math

VALID_RANGE = range(1, 24)

def tile_from_lat_lon(lat: float, 
    lon: float, 
    zoom: int):
    ''' Get tile from lat lon and zoom
    
    Args:
    - lat: latitude in deg.
    - lon: longitude in deg.
    - zoom: zoom level from 1 to 23.
    '''
    if zoom not in VALID_RANGE:
        raise Exception('valid zoom is from 1 to 23.')
    
    if lat > 90 or lat < -90:
        raise Exception('valid latitude is from -90 to 90.')

    if lon > 180 or lon < -180:
        raise Exception('valid longitude is from -180 to 180.')

    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) 
        / math.pi) / 2.0 * n)
    return (xtile, ytile)

def get_recurrent_tiles(
    x: float,
    y: float, 
    curr_zoom: int, 
    target_zoom: int):
    ''' Get tile coordinates from initial tile. 
    
    Args:
    - x: initial tile x.
    - y: initial tile y.
    - curr_zoom: zoom of the initial tile. Eg. 15.
    - target_zoom: zoom of target tiles. Eg. 16.
    '''
    def recurrent_tiles(
        x,
        y, 
        curr_zoom, 
        target_zoom):
    
        diff = target_zoom - curr_zoom
    
        if diff == 0:
            return x, y
        else:
            out = []
            first_tile = (x*2, y*2)
            second_tile = (x*2+1, y*2)
            third_tile = (x*2, y*2+1)
            fourth_tile = (x*2+1, y*2+1)
            tiles = [first_tile, second_tile, 
                third_tile, fourth_tile]
            for t in tiles:
                res = recurrent_tiles(t[0], 
                  t[1], 
                  curr_zoom+1, 
                  target_zoom)
                out.extend(res)
            return out
    
    if curr_zoom > target_zoom:
        raise Exception('current zoom must be'+\
          ' smaller than target zoom.')

    if curr_zoom not in VALID_RANGE or \
        target_zoom not in VALID_RANGE:
        raise Exception('valid zoom is from 1 to 23.')

    tiles = recurrent_tiles(x, y, 
        curr_zoom, 
        target_zoom)
    return [tuple(tiles[i:i + 2]) for i \
      in range(0, len(tiles), 2)]