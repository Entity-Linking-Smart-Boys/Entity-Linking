from named_entity_recognition.NER_spacy import *
from candidate_generation.candidate_generation import *
import json


if __name__ == "__main__":
    text = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."

    entities = named_entity_recognition_using_spacy(text)
    # print(entities)
    entities = map_to_dbpedia_ontology(entities)

    for entity in entities:

        query_result = query_dbpedia(entity)
        print(entity[0])
        # print(json.dumps(query_result, indent=2))  # print formatted json

        print_found_results(query_result)
        print("#####")
