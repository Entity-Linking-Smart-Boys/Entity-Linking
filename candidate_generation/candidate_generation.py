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
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    # # Example: look for an object "Barack_Obama" and get the property "label"
    # sparql.setQuery('''
    #     SELECT ?object
    #     WHERE { dbr:Barack_Obama dbo:label ?object .}
    # ''')

    # WHERE {  ?GPE rdfs:label      "Gdansk"@en }

    sparql.setQuery(f'''
    SELECT ?name ?comment ?image
    WHERE {{ dbr:{entity} rdfs:label ?name.
             dbr:{entity} rdfs:comment ?comment.
             dbr:{entity} dbo:thumbnail ?image.

        FILTER (lang(?name) = 'en')
        FILTER (lang(?comment) = 'en')
    }}''')

    sparql.setReturnFormat(JSON)

    sparql.verify = False
    query_result = sparql.query().convert()

    return query_result


def print_query_result(query_result):
    for result in query_result['results']['bindings']:
        print(result['object'])

        lang, value = result['object']['xml:lang'], result['object']['value']
        # print(f'Lang: {lang}\tValue: {value}')
        if lang == 'en':
            print(value)


def create_graph_from_query():
    """
    Get the parent and child nodes.
    This allows to create a graph of objects (CONSTRUCT).
    Example: Parent - Artificial Intelligence, Child - Markov Models, etc.
    """
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery('''
    CONSTRUCT { dbc:Machine_learning skos:broader ?parent .
                dbc:Machine_learning skos:narrower ?child .} 
    WHERE {
        { dbc:Machine_learning skos:broader ?parent . }
    UNION
        { ?child skos:broader dbc:Machine_learning . }
    }''')

    sparql.setReturnFormat(N3)  # N triples
    query_result = sparql.query().convert()

    g = Graph()
    g.parse(data=query_result, format='n3')
    print(g.serialize(format='ttl'))


def iterate_entities(entities):
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')

    for entity in entities:
        print('###########################################')
        sparql.setQuery(f'''
        SELECT ?name ?comment ?image
        WHERE {{ dbr:{entity} rdfs:label ?name.
                 dbr:{entity} rdfs:comment ?comment.
                 dbr:{entity} dbo:thumbnail ?image.

            FILTER (lang(?name) = 'en')
            FILTER (lang(?comment) = 'en')
        }}''')

        sparql.setReturnFormat(JSON)
        query_result = sparql.query().convert()

        result = query_result['results']['bindings'][0]
        name, comment, image_url = result['name']['value'], result['comment']['value'], result['image']['value']

        print(name)

        # Attempt to open the image with error handling
        try:
            print(f'image_url: {image_url}')
            display(Image(url=image_url, width=100, unconfined=True))
        except Exception as e:
            print(f'Error: {e}')

        print(f'{comment}...')


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    # TODO: map spacy entity types to dbpedia entity types
    # TODO: adjust the sparql query to use the entity type

