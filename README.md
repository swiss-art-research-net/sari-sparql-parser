# SARI Sparql Parser

A parser for SPARQL queries and updates.

Note: This parser is very experimental and may not function very reliably.

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

This will output:
```python
{
    'prefixes': {'crm': 'http://www.cidoc-crm.org/cidoc/crm'},
    'select': ['subject', 'identifier'],
    'where': [{
        's': {'type': rdflib.term.Variable, 'value': 'subject'},
        'p': {'type': rdflib.term.URIRef, 'value': 'http://www.cidoc-crm.org/cidoc/crmP1_is_identified_by'},
        'o': {'type': rdflib.term.Variable, 'value': 'identifier'}
    },
    {
        's': {'type': rdflib.term.Variable, 'value': 'identifier'},
        'p': {'type': rdflib.term.URIRef, 'value': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'},
        'o': {'type': rdflib.term.Variable, 'value': 'type'}
    }],
    'values': [{
        'type': {'type': rdflib.term.URIRef, 'value': 'http://www.cidoc-crm.org/cidoc/crmE41_Appellation'}
    },
    {
        'type': {'type': rdflib.term.URIRef,'value': 'http://www.cidoc-crm.org/cidoc/crmE42_Identifier'}
    }]
}
```
