.PHONY: create-doc

.PHONY: run-tests

.PHONY: build

create-doc:
	pdoc -o ./docs ./ladybug_geojson/

run-tests:
	python -m pytest tests/

build:
	python setup.py sdist bdist_wheel