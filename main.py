from named_entity_recognition.NER_spacy import *
from candidate_generation.candidate_generation import *

if __name__ == "__main__":
    text = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."

    entities = named_entity_recognition_using_spacy(text)
    print(entities)

    for entity in entities:
        string_entity = str(entity).replace(" ", "_")
        query_result = query_dbpedia(string_entity)
        print(string_entity)
        print(query_result)


        # print_query_result(query_result)
        print("#####")
