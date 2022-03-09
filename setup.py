import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="ladybug-geojson",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Convert geojson types into ladybug geometry types.",
    long_description="Convert geojson types into ladybug geometry types.",
    long_description_content_type="text/plain",
    url="https://github.com/pollination/ladybug-geojson",
    packages=setuptools.find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent"
    ],
    license="AGPL-3.0"
)
