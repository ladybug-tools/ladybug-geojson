#!/bin/sh

echo "PyPi Deployment..."
echo "Building distribution"
python setup.py sdist bdist_wheel
echo "Pushing new version to PyPi"
twine upload dist/* -u $PYPI_USERNAME -p $PYPI_PASSWORD
