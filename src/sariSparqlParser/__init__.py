class parser():

    def parseQuery(self, query):
        """
        Parse a SPARQL query.
        :param query: The query to parse
        :return: A dictionary with the following keys:
            - prefixes: A dictionary with the prefixes used in the query
            - select: A list of variables that are projected
            - where: A list of triples that are used in the WHERE clause
            - values: A list of values that are used in the VALUES clause

        >>> query = "PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/> SELECT ?s WHERE { ?s crm:P1_is_identified_by ?o }"
        >>> q = parser()
        >>> q.parseQuery(query)
        {'prefixes': {'crm': 'http://www.cidoc-crm.org/cidoc-crm/'}, 'select': ['s'], 'where': [{'s': {'type': <class 'rdflib.term.Variable'>, 'value': 's'}, 'p': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by'}, 'o': {'type': <class 'rdflib.term.Variable'>, 'value': 'o'}}], 'values': []}

        >>> query = "PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/> SELECT ?s ?o WHERE { ?s crm:P1_is_identified_by ?o . ?o a ?type . VALUES (?type) { (crm:E41_Appellation) (crm:E42_Identifier) } }"
        >>> q.parseQuery(query)
        {'prefixes': {'crm': 'http://www.cidoc-crm.org/cidoc-crm/'}, 'select': ['s', 'o'], 'where': [{'s': {'type': <class 'rdflib.term.Variable'>, 'value': 's'}, 'p': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by'}, 'o': {'type': <class 'rdflib.term.Variable'>, 'value': 'o'}}, {'s': {'type': <class 'rdflib.term.Variable'>, 'value': 'o'}, 'p': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'}, 'o': {'type': <class 'rdflib.term.Variable'>, 'value': 'type'}}], 'values': [{'type': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/E41_Appellation'}}, {'type': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/E42_Identifier'}}]}
        """
        from rdflib.plugins.sparql.parser import parseQuery
        try:
            parsedQuery = parseQuery(query)
        except:
            raise ValueError("Could not parse query",query)
            return False
                
        return {
            "prefixes": self._getPrefixes(parsedQuery),
            "select": self._getProjectionVariables(parsedQuery),
            "where": self._parseTriples(parsedQuery),
            "values": self._parseValues(parsedQuery)
        }
    
    def parseUpdate(self, update):
        """
        Parse a SPARQL update.
        :param update: The update to parse
        :return: A dictionary with the following keys:
            - prefixes: A dictionary with the prefixes used in the update
            - where: A list of triples that are used in the WHERE clause
            - values: A list of values that are used in the VALUES clause

        >>> update = "PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/> INSERT { ?s crm:P1_is_identified_by ?o } WHERE { ?s crm:P1_is_identified_by ?o }"
        >>> u = parser()
        >>> u.parseUpdate(update)
        {'prefixes': {'crm': 'http://www.cidoc-crm.org/cidoc-crm/'}, 'where': [{'s': {'type': <class 'rdflib.term.Variable'>, 'value': 's'}, 'p': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by'}, 'o': {'type': <class 'rdflib.term.Variable'>, 'value': 'o'}}], 'values': []}

        >>> update = "PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/> INSERT { ?s crm:P1_is_identified_by ?o } WHERE { ?s crm:P1_is_identified_by ?o . ?o a ?type . VALUES (?type) { (crm:E41_Appellation) (crm:E42_Identifier) } }"
        >>> u.parseUpdate(update)
        {'prefixes': {'crm': 'http://www.cidoc-crm.org/cidoc-crm/'}, 'where': [{'s': {'type': <class 'rdflib.term.Variable'>, 'value': 's'}, 'p': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by'}, 'o': {'type': <class 'rdflib.term.Variable'>, 'value': 'o'}}, {'s': {'type': <class 'rdflib.term.Variable'>, 'value': 'o'}, 'p': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'}, 'o': {'type': <class 'rdflib.term.Variable'>, 'value': 'type'}}], 'values': [{'type': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/E41_Appellation'}}, {'type': {'type': <class 'rdflib.term.URIRef'>, 'value': 'http://www.cidoc-crm.org/cidoc-crm/E42_Identifier'}}]}
        """
        from rdflib.plugins.sparql.parser import parseUpdate
        try:
            parsedUpdate = parseUpdate(update)
        except:
            raise ValueError("Could not parse update", update)
        return {
            "prefixes": self._getPrefixes(parsedUpdate),
            "where": self._parseTriples(parsedUpdate),
            "values": self._parseValues(parsedUpdate)
        }
        
    def _extractWhereTriples(self, parserOutput):
        from pyparsing import ParseResults
        triplesRaw = []
        if type(parserOutput) is ParseResults:
            for d in parserOutput.asList():
                if 'where' in d:
                    items = d['where'].items()
                    break
        else:
            # Assume SPARQL Update
            items =  parserOutput['request'][0]['where'].items()
        for item in items:
            for rawTriple in item[1][0]['triples']:
                triplesRaw.append(rawTriple)
        return triplesRaw

    def _getPrefixes(self, parserOutput):
        from pyparsing import ParseResults
        if type(parserOutput) is ParseResults and 'prefix' in parserOutput[0][0]:
            prefixesRaw = parserOutput[0]
        if 'prologue' in parserOutput and 'prefix' in parserOutput['prologue'][0][0]:
            prefixesRaw = parserOutput['prologue'][0]
        prefixes = {}
        for d in prefixesRaw:
            prefixes[d['prefix']] = str(d['iri'])
        return prefixes
    
    def _getProjectionVariables(self, parsedQuery):
        variables = []
        for d in parsedQuery.asList():
            if 'projection' in d:
                for var in d['projection']:
                    variables.append(str(var['var']))
        return variables
    
    def _getTypeOfTerm(self, term):
        from rdflib.term import Variable, URIRef, Literal
        if type(term) is Variable:
            return Variable
        if 'string' in term:
            return Literal
        else:
            return URIRef

    def _getValueOfTerm(self, term, prefixes):
        from rdflib.term import Variable, URIRef, Literal
        t = self._getTypeOfTerm(term)
        if t is Variable:
            return str(term)
        if t is URIRef:
            try:
                part = term['part'][0]['part'][0]['part']
            except:
                part = term
            if 'prefix' in part:
                prefix = prefixes[part['prefix']]
                localname = part['localname']
                return prefix + localname
            else:
                return str(part)
        if t is Literal:
            return str(term['string'])
        return False

    def _parseTriples(self, parsedOutput):
        from math import floor
        prefixes = self._getPrefixes(parsedOutput)
        triples = []
        triplesRaw = self._extractWhereTriples(parsedOutput)
        iteration = 0
        prevSet = 0
        prevIteration = 0
        iteration = prevIteration
        triple = {}
        for s, queryPath in enumerate(triplesRaw):
            for i, statement in enumerate(queryPath):
                if iteration != prevIteration or s != prevSet:
                    triples.append(triple)
                    triple = {}
                    prevSet = s
                    prevIteration = iteration
                iteration = floor(i/3)
                if i%3 == 0:
                    key = "s"
                elif i%3 == 1:
                    key = "p"
                elif i%3 == 2:
                    key = "o"

                triple[key] =  {
                    "type": self._getTypeOfTerm(statement),
                    "value": self._getValueOfTerm(statement, prefixes)
                }
        triples.append(triple)
        # For statements missing a subject, take the subject from the previous statement.
        # Afterwards remove statements missing a predicate and object. These artefacts stem 
        # from tense notation.
        for i, triple in enumerate(triples):
            if not 's' in triple:
                if i > 0 and 's' in triples[i-1]:
                    triple['s'] = triples[i-1]['s']
        return [d for d in triples if 's' in d and 'p' in d and 'o' in d]
    
    def _parseValues(self, parserOutput):
        from pyparsing import ParseResults
        prefixes = self._getPrefixes(parserOutput)
        
        try:
            if type(parserOutput) is ParseResults:
                valuesRaw = parserOutput.asList()[1]['where']['part'][1]
            else:
                valuesRaw = parserOutput['request'][0]['where']['part'][1]
        except:
            # No values present
            return []
        keys = {}
        for i, v in enumerate(valuesRaw['var']):
            keys[i] = str(v)
        data = []
        for values in valuesRaw['value']:
            row = {}
            for i, statement in enumerate(values):
                row[keys[i]] =  {"type": self._getTypeOfTerm(statement),
                                "value": self._getValueOfTerm(statement, prefixes)}
            data.append(row)
        return data


if __name__ == '__main__':
    import doctest
    doctest.testmod()
