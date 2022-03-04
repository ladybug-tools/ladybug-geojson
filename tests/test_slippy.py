# coding=utf-8
import pytest
from ladybug_geojson.slippy.map import ( tile_from_lat_lon,
    get_recurrent_tiles )


def test_tile_from_lat_lon():
    coord = (41.894599, 12.483092)
    pt = tile_from_lat_lon(*coord, 15)
    
    assert 17520 in pt

def test_get_recurrent_tiles():

    tiles = get_recurrent_tiles(17515, 12173, 15, 16)
    assert (35031, 24346) in tiles
    assert len(tiles) == 4
