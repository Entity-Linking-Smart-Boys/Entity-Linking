class Entity:
    """
    This class stores entity information.
    One entity can have multiple candidates got from Knowledge Base.
    """
    surface_form = ""  # the string in text representing the entity (SPACY: text)
    ont_type_spacy = ""  # type of entity from NER (SPACY: label_)
    start_char = 0  # Index of start of entity in the text (SPACY: start_char)
    end_char = 0  # Index of end of entity in the text (SPACY: end_char)
    ont_type_dbpedia = ""  # from DBpedia - mapped type from spacy to dbpedia; one or more type possible
    candidates = []  # list of potential candidates for linking
    sentence_text = ""  # string: the sentence in which the entity was detected
    sentence_number = 0  # number of the sentence in which the entity was detected; counting starts from 0
