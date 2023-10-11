import spacy
from spacy import displacy


def print_tokens(doc):
    sentences = list(doc.sents)
    print(sentences)
    # tokenization
    for token in doc:
        print(token.text)


def named_entity_recognition_using_spacy(text):
    nlp = spacy.load('en_core_web_lg')

    # Load the text and process it
    text = (
        "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system.")

    doc = nlp(text)

    # print_tokens(doc)

    # print entities
    entities = [(e.text, e.label_, e.start_char, e.end_char) for e in doc.ents]
    # print(entities)  # [('Nikola Tesla', 0, 12, 'PERSON'), ('Serbian', 14, 21, 'NORP'), ('Тесла', 39, 44, 'PERSON'), ('Serbian', 52, 59, 'NORP')]
    # displacy allows to see the text in a user-friendly form with tagged entities
    # print(doc.ents)  # (Nikola Tesla, Serbian, Тесла, Serbian)
    displacy.render(doc, style='ent')

    return list(entities)


def map_entity_type(entity):
    spacy_to_dbpedia_ontology_mapping = {
        "PERSON": "Person",
        "NORP": "Group",
        "FAC": "Place",
        "ORG": "Organization",
        "GPE": "Place",
        "LOC": "Place",
        "EVENT": "Event",
        "WORK_OF_ART": "Work",
        "LAW": "Document",
        "LANGUAGE": "Language"
    }
    entity_type = entity[1]
    entity[1] = spacy_to_dbpedia_ontology_mapping.get(entity_type)
    return entity


def map_to_dbpedia_ontology(entities):
    mapped_entities = []
    for entity in entities:
        mapped_entity = map_entity_type(list(entity))
        mapped_entities.append(mapped_entity)
    return mapped_entities


if __name__ == "__main__":
    text = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."

    # entities = named_entity_recognition_using_spacy(text)
    # print(entities)
    # mapped_entities = []
    # for entity in entities:
    #     mapped_entity = map_entity_type(list(entity))
    #     mapped_entities.append(mapped_entity)
    #     print(mapped_entity)

