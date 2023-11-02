from named_entity_recognition.NER_using_spacy import *
from candidate_generation.candidate_generation import *
from candidate_disambiguation.candidate_disambiguation import *
import time


def get_text_from_file(filename):
    with open(filename, encoding='utf8') as f:
        text_from_file = f.readlines()
    return ''.join(text_from_file).replace('\n', ' ')


def print_candidates_for_each_entity(list_of_entities):
    """
    Print list of candidates for each found entity.
    """
    for entity in list_of_entities:
        print(f"\nEntity \"{entity.surface_form}\"")
        print(f"ont_type_spacy \"{entity.ont_type_spacy}\"")
        print(f"ont_type_dbpedia \"{entity.ont_type_dbpedia}\"")
        print(f"Candidates ({len(entity.candidates)})")
        # for candidate in entity.candidates:
        #     print(f"\tName: {candidate.label}, URI: {candidate.uri}")
        print("\n")


def try_to_map_all_entities_to_dbpedia_ont(entities):
    entities_to_remove = []
    for entity in entities:
        entity = map_entity_type_to_dbpedia_ontology(entity)
        if entity.ont_type_dbpedia is None:
            entities_to_remove.append(entity)  # Add the entity to the list of entities to remove

    # Remove the entities that couldn't be mapped
    for entity in entities_to_remove:
        entities.remove(entity)

    return entities


def print_disambiguated_entities(entities):
    for entity in entities:
        # Print the entity label
        print("Entity Label:", entity.surface_form)

        # Iterate through the candidates for the current entity
        for candidate in entity.candidates[:5]:
            # Print the candidate's partial score and similarity score
            print("Candidate label:", candidate.label)
            print("Candidate uri:", candidate.uri)
            print("Candidate Partial Score:", candidate.cand_dis_partial_score)
            print("Candidate Similarity Score:", candidate.cand_dis_by_similarity_in_dbpedia_graph)
            print('\n')
        print('\n\n')


if __name__ == "__main__":
    start_time = time.time()  # Record the start time

    text_to_analyze = get_text_from_file('text_to_analyse.txt')

    # Named Entity Recognition using Spacy
    ner_start_time = time.time()
    entities = named_entity_recognition_using_spacy(text_to_analyze)
    ner_end_time = time.time()
    print(f"Named Entity Recognition took {ner_end_time - ner_start_time} seconds")

    entities = try_to_map_all_entities_to_dbpedia_ont(entities)

    # Finding candidates
    query_start_time = time.time()
    for entity in entities:
        query_result = query_dbpedia(entity)
        entity = save_found_candidates(query_result, entity)
    query_end_time = time.time()
    print(f"Finding candidates took {query_end_time - query_start_time} seconds")

    print_candidates_for_each_entity(entities)

    # Disambiguate candidates
    disambiguate_start_time = time.time()
    entities = disambiguate_candidates(entities, text_to_analyze)
    disambiguate_end_time = time.time()
    print(f"Disambiguating candidates took {disambiguate_end_time - disambiguate_start_time} seconds")

    print_disambiguated_entities(entities)

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(f"Total time taken for the entire process: {total_time} seconds")