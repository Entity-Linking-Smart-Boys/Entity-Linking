from named_entity_recognition.NER_using_spacy import *
from candidate_generation.candidate_generation import *


def print_candidates_for_each_entity(list_of_entities):
    """
    Print list of candidates for each found entity.
    """
    for entity in list_of_entities:
        print(f"\nEntity \"{entity.surface_form}\"")
        print(f"ont_type_spacy \"{entity.ont_type_spacy}\"")
        print(f"ont_type_dbpedia \"{entity.ont_type_dbpedia}\"")
        print(f"Candidates ({len(entity.candidates)}):")
        for candidate in entity.candidates:
            print(f"\tName: {candidate.label}, URI: {candidate.uri}")
        print("\n")


if __name__ == "__main__":
    with open('text_to_analyse.txt', encoding='utf8') as f:
        text_to_analyse = f.readlines()

    entities = named_entity_recognition_using_spacy(text_to_analyse)

    for entity in entities:
        entity = map_entity_type_to_dbpedia_ontology(entity)
        query_result = query_dbpedia(entity)

        entity = save_found_candidates(query_result, entity)

    print_candidates_for_each_entity(entities)
