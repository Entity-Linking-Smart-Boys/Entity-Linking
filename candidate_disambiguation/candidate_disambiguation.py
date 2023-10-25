from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def calculate_similarity(entity_label, candidate_label):
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

    :param entities: A list of entity objects with associated candidates.
    :return: Updated entities with candidates containing Levenshtein distance-based similarity scores.

    This function calculates the Levenshtein distance-based similarity scores between
    the entity labels and candidate labels for each entity and its candidates.
    The calculated similarity scores are stored in the candidates
    and returned as the updated entity list.
    """

    for entity in entities:
        for candidate in entity.candidates:
            entity_label = entity.surface_form
            candidate_label = str(candidate.label).replace("_", " ")
            similarity = calculate_similarity(entity_label, candidate_label)
            candidate.cand_dis_by_levenshtein_score = similarity

    return entities


def disambiguate_by_context(entities):
    """
    Disambiguate candidates for each entity based on context similarity.

    :param entities: List of entities found in the text, each with associated candidates.
    :return: List of entities with candidates ranked from the most probable to least probable, based on context.
    """

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

    return entities


def disambiguate_candidates(entities, text):
    """
    Disambiguate candidates for each entity.

    :param entities: list of entities found in the text and categorized into DBpedia ontology
    :param text: text to analyse (original)
    :return: entities with candidates ranked from the most probable to least probable
    """
    entities = disambiguate_by_context(entities)
    entities = disambiguate_by_levenshtein_distance(entities)

    return entities
