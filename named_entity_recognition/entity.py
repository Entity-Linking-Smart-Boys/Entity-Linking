class Entity:
    """
    Class stores entity information.
    One entity can have multiple candidates got from Knowledge Base.
    """
    surface_form = ""  # the string in text representing the entity
    ont_type_spacy = ""  # type of entity from NER
    ont_type_dbpedia = ""  # from DBpedia - mapped type from spacy to dbpedia; one or more type possible
    candidates = []  # list of potential candidates for linking

