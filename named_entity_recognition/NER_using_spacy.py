import spacy
from spacy import displacy
from named_entity_recognition.entity import Entity


def named_entity_recognition_using_spacy(text):
    nlp = spacy.load('en_core_web_lg')

    doc = nlp(text)

    entities = [(e.text, e.label_, e.start_char, e.end_char) for e in doc.ents]

    displacy.render(doc, style='ent')

    entity_to_return = []
    for entity in list(entities):
        new_entity = Entity()
        new_entity.surface_form = entity[0]
        new_entity.ont_type_spacy = entity[1]

        entity_to_return.append(new_entity)

    return entity_to_return


def map_entity_type_to_dbpedia_ontology(entity):
    spacy_to_dbpedia_ontology_mapping = {
        "PERSON": "dbo:Species, dbo:Agent",  # People, including fictional.
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