# SARI Sparql Parser

A parser for SPARQL queries and updates

## Installation

install using pip


```sh
pip install sari-sparql-parser
```

## Usage

Parse a SPARQL query:

```python
from sariSparqlParser import parser

query = """PREFIX crm: <http://www.cidoc-crm.org/cidoc/crm>
    SELECT ?subject ?identifier WHERE {
        ?subject crm:P1_is_identified_by ?identifier .
        ?identifier a ?type .
        VALUES (?type) {
            (crm:E41_Appellation)
            (crm:E42_Identifier)
        }
    }
"""
p = parser()
p.parseQuery(query)
```
