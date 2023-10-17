from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import rdflib
from .candidate import Candidate


def merge_jsons(main_results, new_results):
    if main_results != "":
        # Merge the two dictionaries
        main_results.update(new_results)

        return main_results
    else:
        return new_results  # return only this, because main results are empty


def query_dbpedia(entity):
    """
    Create the Query and send it via SPARQLWrapper.

    :param entity: entity to query about
    :return: query result
    """

    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    dbpedia_ont_types = entity.ont_type_dbpedia.split(',')

    results = ""

    for ontology_type in dbpedia_ont_types:
        query = '''
            PREFIX dbo: <http://dbpedia.org/ontology/>
           
            SELECT ?entity ?typeValue ?name
            WHERE {
              {
                ?entity a/rdfs:subClassOf* ''' + ontology_type + ''';
                        rdfs:label ?name ;
                        a ?type .
                BIND ("''' + ontology_type + '''" as ?typeValue)
                FILTER (langMatches(lang(?name), "en") && CONTAINS(?name, "''' + entity.surface_form + '''") && STRSTARTS(STR(?type), "http://dbpedia.org/ontology"))
              }
            }
            group by ?entity  # this lowers the number of results
        '''

        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)

        sparql.verify = False
        query_result = sparql.query().convert()
        results = merge_jsons(results, query_result)
    return results


def save_found_candidates(json_data, entity):
    entity.candidates = []
    for result in json_data["results"]["bindings"]:
        candidate_uri = result["entity"]["value"]
        candidate_label = result["name"]["value"]
        candidate_type = result["typeValue"]["value"]
        candidate = Candidate(candidate_uri, candidate_label, candidate_type)
        entity.candidates.append(candidate)
    return entity


def sort_cand_by_ont_depth(entity):
    # Load the DBpedia ontology RDF file
    ontology_file = "candidate_generation/dbpedia_ontology.rdf"
    g = rdflib.Graph()
    g.parse(ontology_file, format="xml")

    # calculate the ont depth
    for cand in entity.candidates:
        # Define the class you're interested in
        target_class = rdflib.URIRef(str(cand.ont_type))

        # Calculate the depth of the target class
        visited = set()
        cand.ont_type_depth = calculate_depth(target_class, visited, g)

    # Sort the candidates for each entity by ont_type_depth
    entity.candidates = sorted(entity.candidates, key=lambda x: (x.name, x.ont_type_depth))

    return entity


def calculate_depth(current_class, visited, g):
    if current_class == rdflib.OWL.Thing:
        return 0  # Top-level class reached
    else:
        superclasses = list(g.transitive_objects(current_class, rdflib.RDFS.subClassOf))
        depths = []
        for cls in superclasses:
            if cls not in visited:
                visited.add(cls)
                depth = calculate_depth(cls, visited, g)
                visited.remove(cls)
                depths.append(depth)

        if not depths:
            return 1  # No superclasses, so depth is 1
        else:
            return 1 + max(depths)


def extract_deepest_candidates(entity):
    # Create a dictionary to keep track of the highest ont_type_depth for each name
    highest_ont_type_depth = {}
    new_candidates = []
    for candidate in entity.candidates:
        if candidate.name not in highest_ont_type_depth:
            highest_ont_type_depth[candidate.name] = candidate.ont_type_depth
        elif candidate.ont_type_depth > highest_ont_type_depth[candidate.name]:
            highest_ont_type_depth[candidate.name] = candidate.ont_type_depth

    # Replace the current list of candidates with only the deepest candidates
    new_candidates = [candidate for candidate in entity.candidates if
                      candidate.ont_type_depth == highest_ont_type_depth[candidate.name]]
    entity.candidates = new_candidates
    return entity


if __name__ == "__main__":
    pass
