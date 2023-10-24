from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
from .candidate import Candidate


def merge_results(new_results, main_results):
    """
    Merge two dictionaries containing results from SPARQL query.

    :param new_results: results with entities of new ontology type
    :param main_results: results with entities of old ontology types
    :return: merged results as dictionary
    """
    # Merge the 'bindings' lists from both dictionaries
    main_results['results']['bindings'].extend(new_results['results']['bindings'])
    return main_results


def query_dbpedia(entity):
    """
    Create SPARQL query and send it via SPARQLWrapper.

    :param entity: entity containing details used during creation of query
    :return: query result
    """

    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    dbpedia_ont_types = entity.ont_type_dbpedia.split(',')

    results = {
        "head": {
            "link": [],
            "vars": ["entity", "typeValue", "name", "abstract"]
        },
        "results": {
            "distinct": False,
            "ordered": True,
            "bindings": []
        }
    }

    for ontology_type in dbpedia_ont_types:
        query = '''
            PREFIX dbo: <http://dbpedia.org/ontology/>
           
            SELECT ?entity ?typeValue ?name ?abstract
            WHERE {
              {
                ?entity a/rdfs:subClassOf* ''' + ontology_type + ''';
                        rdfs:label ?name ;
                        a ?type ;
                        dbo:abstract ?abstract.
                BIND ("''' + ontology_type + '''" as ?typeValue)
                FILTER (langMatches(lang(?name), "en") && CONTAINS(?name, "''' + entity.surface_form + '''") && STRSTARTS(STR(?type), "http://dbpedia.org/ontology") && langMatches(lang(?abstract), "en"))
              }
            }
            group by ?entity  # this lowers the number of results
        '''

        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)

        sparql.verify = False
        query_result = sparql.query().convert()
        results = merge_results(query_result, results)
    return results


def save_found_candidates(query_results, entity):
    """
    Extract data from SPARQL query results and save it into candidate instances.
    The list of candidates is saved into the entity.

    :param query_results: results of SPARQL query
    :param entity: entity in which the candidates are saved into
    :return: updated entity with list of candidates
    """
    entity.candidates = []
    for result in query_results["results"]["bindings"]:
        candidate_uri = result["entity"]["value"]
        candidate_label = result["name"]["value"]
        candidate_type = result["typeValue"]["value"]

        # if abstract exists:
        if result["abstract"]["value"]:
            abstract = result["abstract"]["value"]
            candidate = Candidate(candidate_uri, candidate_label, candidate_type, abstract)
        else:
            candidate = Candidate(candidate_uri, candidate_label, candidate_type)
        entity.candidates.append(candidate)
    return entity


if __name__ == "__main__":
    pass
