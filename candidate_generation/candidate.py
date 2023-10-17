class Candidate:
    """
    Class stores candidate information.
    Each candidate is assigned to specific entity.
    """
    def __init__(self, uri, label, ont_type):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label  # from DBpedia - rdfs:label value
        self.ont_type = ont_type  # from DBpedia - ontology type
