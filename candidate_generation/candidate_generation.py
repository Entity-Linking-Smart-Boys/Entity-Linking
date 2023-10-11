from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import ssl
from IPython.display import display, Image


def query_dbpedia(entity):
    """
    Create the Query and send it via SPARQLWrapper.

    :param entity: entity to query about
    :return: query result
    """

    # variables used to create a query
    surface_form = entity[0]
    ontology_type = entity[1]

    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    # create the query
    sparql.setQuery(f'''
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dct: <http://purl.org/dc/terms/>
        
        SELECT ?entity ?abstract
        WHERE {{  ?entity rdf:type dbo:{ontology_type} ;
                    rdfs:label ?name ;
                    dbo:abstract ?abstract .
         
          
          FILTER (langMatches(lang(?name), "en") && CONTAINS(?name, "{surface_form}") && langMatches(lang(?abstract), "en"))
        }}
        LIMIT 5
    ''')

    sparql.setReturnFormat(JSON)

    sparql.verify = False
    query_result = sparql.query().convert()

    return query_result


def print_found_results(json_data):
    for result in json_data["results"]["bindings"]:
        uri = result["entity"]["value"]
        abstract = result["abstract"]["value"]
        resource_name = uri.split('/')[-1]

        print(resource_name, uri, abstract[:40])
