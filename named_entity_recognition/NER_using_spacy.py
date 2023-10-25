import spacy
from spacy import displacy
from named_entity_recognition.entity import Entity


def named_entity_recognition_using_spacy(text):
    """
    Perform Named Entity Recognition (NER) using spaCy (Docs: https://spacy.io/api/entityrecognizer).

    :param text: text to annotate
    :return: found entities with specific surface form, label, and sentence number.
    """
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text)

    entities = [(e.text, e.label_, e.start_char, e.end_char, e.sent) for e in doc.ents]

    # Use displacy to visualize the entities (optional)
    displacy.render(doc, style='ent')

    found_entities = []
    for entity in entities:
        new_entity = Entity()
        new_entity.surface_form = entity[0]
        new_entity.ont_type_spacy = entity[1]
        new_entity.start_char = entity[2]
        new_entity.end_char = entity[3]
        new_entity.sentence_number = list(doc.sents).index(entity[4])
        new_entity.sentence_text = str(entity[4])

        found_entities.append(new_entity)

    return found_entities


def map_entity_type_to_dbpedia_ontology(entity):
    """
    Map the spaCy type of entity into the types of DBpedia ontology.
    This method allows to specify the type of entity in terms of DBpedia ontology and create effective SPARQL queries.

    :param entity: entity to map
    :return:
    """
    spacy_to_dbpedia_ontology_mapping = {
        "PERSON": "dbo:Species",  # People, including fictional.
        "NORP": "dbo:Agent, dbo:Species",  # Nationalities or religious or political groups.
        "FAC": "dbo:Building, dbo:ArchitecturalStructure, dbo:Infrastructure",  # Buildings, airports, highways, bridges, etc.
        "ORG": "dbo:Agent",  # Companies, agencies, institutions, etc.
        "GPE": "dbo:Place, dbo:Agent, dbo:Building",  # Countries, cities, states.
        "LOC": "dbo:Place",  # Non-GPE locations, mountain ranges, bodies of water.
        "PRODUCT": "dbo:MeanOfTransportation, dbo:Food, dbo:Device",  # Objects, vehicles, foods, etc. (Not services.)
        "EVENT": "dbo:Event",  # Named hurricanes, battles, wars, sports events, etc.
        "WORK_OF_ART": "dbo:Work",  # Titles of books, songs, etc.
        "LAW": "dbo:Work",  # Named documents made into laws.
        "LANGUAGE": "dbo:Language",  # Any named language.
        # DATE:       #  Absolute or relative dates or periods.
        # TIME:       # Times smaller than a day.
        # PERCENT:   #   Percentage, including ”%“.
        # MONEY:     #   Monetary values, including unit.
        # QUANTITY:  #   Measurements, as of weight or distance.
        # ORDINAL:   #   “first”, “second”, etc.
        "CARDINAL": "dbo:TopicalConcept"  # Numerals that do not fall under another type.
    }

    entity.ont_type_dbpedia = spacy_to_dbpedia_ontology_mapping.get(entity.ont_type_spacy)

    return entity


if __name__ == "__main__":
    pass