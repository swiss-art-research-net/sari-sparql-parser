import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="sari-sparql-parser",
    version="0.0.5",
    author="Florian Kräutli",
    author_email="florian.kraeutli@uzh.ch",
    description="A library for parsing SPARQL queries and updates",
    include_package=True,
    install_requires=['rdflib','pyparsing'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swiss-art-research-net/sari-sparql-parser.git",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)