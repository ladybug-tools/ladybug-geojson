.PHONY: create-doc

.PHONY: run-tests

create-doc:
	pdoc -o ./docs ./ladybug_geojson/

run-tests:
	python -m pytest tests/
