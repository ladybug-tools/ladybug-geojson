# ladybug-geojson

A library to convert geojson types into ladybug geometry types.

# docs
[API Documentation](https://www.ladybug.tools/ladybug_geojson/docs/)

# examples

### generate ladybug geometry from geojson string
```python
from ladybug_geojson.convert.geojson import from_geojson
geojson = '''
    { "type": "FeatureCollection",
    "features": [
        { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
        "properties": {"prop0": "value0"}
        },
        { "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
            [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
            ]
            },
        "properties": {
            "prop0": "value0",
            "prop1": 0.0
            }
        },
        { "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
            [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                [100.0, 1.0], [100.0, 0.0] ]
            ]

        },
        "properties": {
            "prop0": "value0",
            "prop1": {"this": "that"}
            }
        }
        ]
    }
    '''
objs = from_geojson(geojson)
```

# make commands
- Generate docs: `make create-doc`
- Run tests: `make run-tests`
- Generate package manually: `make build`

## todo
- [ ] future release - add from_geometry and to_geojson
