from named_entity_recognition.NER_using_spacy import *
from candidate_generation.candidate_generation import *
from candidate_disambiguation.candidate_disambiguation import *


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
        print(f"Candidates ({len(entity.candidates)}):")
        for candidate in entity.candidates:
            print(f"\tName: {candidate.label}, URI: {candidate.uri}")
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


if __name__ == "__main__":
    text_to_analyse = get_text_from_file('text_to_analyse.txt')

    entities = named_entity_recognition_using_spacy(text_to_analyse)

    entities = try_to_map_all_entities_to_dbpedia_ont(entities)

    for entity in entities:
        query_result = query_dbpedia(entity)
        entity = save_found_candidates(query_result, entity)

    print_candidates_for_each_entity(entities)

    disambiguate_candidates(entities, text_to_analyse)
