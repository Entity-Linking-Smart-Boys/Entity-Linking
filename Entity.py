class Entity:
    surface_form = ""  # the string in text representing the entity
    ont_type_spacy = ""  # type of entity from NER
    ont_type_dbpedia = ""  # from DBpedia - mapped type from spacy to dbpedia; one or more type possible
    resource_name = ""
    candidates = []  # list of potential candidates for linking


class Candidate:
    def __init__(self, uri, label, ont_type):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label
        self.ont_type = ont_type
