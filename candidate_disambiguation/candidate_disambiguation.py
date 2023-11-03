from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
from urllib.parse import quote


def calculate_levenshtein_distance_between_two_strings(entity_label, candidate_label):
    """
    Calculate the similarity score between an entity label and a candidate label using Levenshtein distance.

    :param entity_label: The label of the entity (e.g., the surface form).
    :param candidate_label: The label of the candidate.
    :return: The similarity score between 0 and 1, where higher values indicate greater similarity.

    This function uses Levenshtein distance to measure the similarity between two strings.
    It calculates the Levenshtein distance between the entity label and the candidate label,
    and then converts it into a similarity score.

    Note: A lower Levenshtein distance indicates higher similarity,
    so the similarity score is inversely proportional to the Levenshtein distance.
    """

    # Calculate Levenshtein distance
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    # Calculate Levenshtein distance
    levenshtein_distance_value = levenshtein_distance(entity_label, candidate_label)

    # Calculate similarity score using Levenshtein distance
    # The similarity score is inversely proportional to the Levenshtein distance
    similarity_score = 1 / (1 + levenshtein_distance_value)

    return similarity_score


def disambiguate_by_levenshtein_distance(entities):
    """
    Disambiguate candidate entities for each entity using Levenshtein distance-based similarity scores.
    This function compares two strings:
    - the entity label (surface form)
    - the candidate label of this entity (DBpedia label)
    This function calculates the Levenshtein distance-based similarity scores between
    the entity labels and candidate labels for each entity and its candidates.
    The calculated similarity scores are stored in the candidates
    and returned as the updated entity list.

    :param entities: A list of entity objects with associated candidates.
    :return: Updated entities with candidates containing Levenshtein distance-based similarity scores.
    """

    for entity in entities:
        for candidate in entity.candidates:
            entity_label = entity.surface_form
            candidate_label = str(candidate.label).replace("_", " ")
            levenshtein_distance_score = calculate_levenshtein_distance_between_two_strings(entity_label, candidate_label)
            candidate.cand_dis_by_levenshtein_score = levenshtein_distance_score
            candidate.cand_dis_current_score += levenshtein_distance_score

    return entities







def disambiguate_by_context_sentence_and_abstract(entities):
    """
    Disambiguate candidates for each entity based on context similarity.
    Two strings are compared:
    - the sentence in which the entity was recognized
    - the abstract of the candidate of the recognized entity
    The similarity between the two strings is calculated using TF-IDF and cosine similarity.

    :param entities: List of entities found in the text, each with associated candidates.
    :return: List of entities with candidates ranked from the most probable to least probable, based on context.
    """
    # TODO: add normalization:
    #   Normalization is an optional step in the TF-IDF calculation,
    #   and it's often used to ensure that the vectors
    #   have a unit length (a magnitude of 1).
    #   Normalization can be achieved using various techniques,
    #   with the most common one being L2 normalization (also known as Euclidean normalization).

    # Create a dictionary to store the first sentence of each abstract by URI
    abstracts = {}

    # Iterate through entities and extract the first sentence of the abstract for each candidate
    for entity in entities:
        if entity.candidates:
            for candidate in entity.candidates:
                abstract = candidate.abstract
                if abstract:
                    abstracts[candidate.uri] = candidate.abstract.split('.')[0]  # Extract the first sentence

    # Calculate TF-IDF for the extracted sentences
    all_sentences = list(abstracts.values()) + [entity.sentence_text for entity in entities if entity.sentence_text]  # Combine abstract sentences and entity sentences
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_sentences)

    # Iterate through entities and calculate similarity
    for entity in entities:
        if entity.candidates:
            entity_sentence = entity.sentence_text  # Sentence of the entity
            if entity_sentence:
                tfidf_entity = tfidf_vectorizer.transform([entity_sentence])

                for candidate in entity.candidates:
                    candidate_sentence = abstracts.get(candidate.uri, '')  # Get the abstract of the candidate
                    tfidf_candidate = tfidf_vectorizer.transform([candidate_sentence])
                    similarity_score = linear_kernel(tfidf_entity, tfidf_candidate).flatten()[0]

                    # Store the score in the candidate instance
                    candidate.cand_dis_by_context_score = similarity_score
                    candidate.cand_dis_current_score += similarity_score

    return entities








def sort_candidates_by_current_score(entities):
    for entity in entities:
        if entity.candidates:
            entity.candidates.sort(key=lambda candidate: candidate.cand_dis_current_score, reverse=True)

    return entities


def normalize_connectivity_in_dbpedia_scores(entities):
    for entity in entities:
        if entity.candidates:
            # Get the minimum and maximum similarity scores in the entity
            min_score = min(candidate.cand_dis_by_connectivity_in_dbpedia_graph_score for candidate in entity.candidates)
            max_score = max(candidate.cand_dis_by_connectivity_in_dbpedia_graph_score for candidate in entity.candidates)
            print(min_score, max_score)
            # Normalize the scores for each candidate
            for candidate in entity.candidates:
                if max_score == min_score:
                    normalized_similarity_score = 1.0  # All scores are the same
                else:
                    normalized_similarity_score = (candidate.cand_dis_by_connectivity_in_dbpedia_graph_score - min_score) / (
                                                             max_score - min_score)
                candidate.cand_dis_normalized_connectivity_in_dbpedia_graph_score = normalized_similarity_score
                candidate.cand_dis_current_score += normalized_similarity_score

    return entities


def find_two_closests_entities(entities, n):
    # n --> Index of the n-th entity
    if n < 0 or n >= len(entities):
        # Entity index out of range
        return None, None

    n_entity = entities[n]

    closest_left_entity = None
    closest_right_entity = None

    # Initialize the minimum distance to a large value
    min_left_distance = float("inf")
    min_right_distance = float("inf")

    for i, entity in enumerate(entities):
        if i == n:
            continue  # Skip the n-th entity itself

        # Calculate the distance between the n-th entity and the current entity
        if entity.end_char < n_entity.start_char:
            left_distance = n_entity.start_char - entity.end_char
            if left_distance < min_left_distance:
                min_left_distance = left_distance
                closest_left_entity = entity
        elif entity.start_char > n_entity.end_char:
            right_distance = entity.start_char - n_entity.end_char
            if right_distance < min_right_distance:
                min_right_distance = right_distance
                closest_right_entity = entity

    return closest_left_entity, closest_right_entity


def calculate_connectivity_for_candidate(center_entity_candidate, left_entity_candidates, right_entity_candidates):
    # Initialize the total similarity score
    total_similarity_score = 0

    # Set up the SPARQL endpoint
    ssl._create_default_https_context = ssl._create_unverified_context  # set the SSL Certificate
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')  # initialize SPARQL Wrapper

    total_similarity_score = query_side_entity_candidates(center_entity_candidate, left_entity_candidates, sparql,
                                                          total_similarity_score)
    total_similarity_score = query_side_entity_candidates(center_entity_candidate, right_entity_candidates, sparql,
                                                          total_similarity_score)

    return total_similarity_score


def query_side_entity_candidates(center_entity_candidate, side_entity_candidates, sparql, total_similarity_score):
    for i in range(0, len(side_entity_candidates)):
        # Encode the entity labels
        center_entity_label = quote(str(center_entity_candidate.label).replace(' ', '_'))
        side_entity_label = quote(str(side_entity_candidates[i].label).replace(' ', '_'))

        query = """
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX dbr: <http://dbpedia.org/resource/> 

            SELECT ?connection (count(?connection) as ?count) 

            WHERE { 

              dbr:""" + center_entity_label + """ ?connection ?x . 

              ?x ?y dbr:""" + side_entity_label + """ . 

              FILTER (?connection = dbo:wikiPageWikiLink) 
            } 
        """
        # print(query)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            # Execute the query
            results = sparql.query().convert()
            # Check if there are results
            if "results" in results and "bindings" in results["results"]:
                count = int(results["results"]["bindings"][0]["count"]["value"])
                total_similarity_score += count
                print("count:" + str(count))
        except IndexError:
            # Handle the case where no results are found
            print(f"No results found for the SPARQL query.")
        except Exception as e:
            print(f"Error executing SPARQL query: {str(e)}")
    return total_similarity_score


def disambiguate_by_dbpedia_graph_connectivity(entities):
    for i, entity in enumerate(entities):
        closest_left_entity, closest_right_entity = find_two_closests_entities(entities, i)

        # Get the top candidates for the centre entity, left entity, and right entity
        top_candidates_count = 5
        current_entity_candidates = entity.candidates[:top_candidates_count]
        left_entity_candidates = closest_left_entity.candidates[:top_candidates_count] if closest_left_entity else []
        right_entity_candidates = closest_right_entity.candidates[:top_candidates_count] if closest_right_entity else []

        # Calculate the connectivity in the DBpedia graph for the selected candidates
        for candidate in current_entity_candidates:
            # Calculate similarity with candidates from the left entity and the right entity
            candidate_total_connectivity_score = calculate_connectivity_for_candidate(candidate,
                                                                                      left_entity_candidates,
                                                                                      right_entity_candidates)

            candidate.cand_dis_by_connectivity_in_dbpedia_graph_score = candidate_total_connectivity_score

    entities = normalize_connectivity_in_dbpedia_scores(entities)

    return entities


def disambiguate_candidates(entities):
    """
    Disambiguate candidates for each entity.

    :param entities: list of entities found in the text and categorized into DBpedia ontology
    :return: entities with candidates ranked from the most probable to the least probable
    """
    entities = disambiguate_by_context_sentence_and_abstract(entities)
    entities = sort_candidates_by_current_score(entities)

    entities = disambiguate_by_levenshtein_distance(entities)
    entities = sort_candidates_by_current_score(entities)

    entities = disambiguate_by_dbpedia_graph_connectivity(entities)
    entities = sort_candidates_by_current_score(entities)

    return entities

