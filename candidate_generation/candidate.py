class Candidate:
    """
    Class stores candidate information.
    Each candidate is assigned to specific entity.
    """

    def __init__(self, uri, label, ont_type, abstract=""):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label  # from DBpedia - rdfs:label value
        self.ont_type = ont_type  # from DBpedia - ontology type
        self.abstract = abstract  # from DBpedia - entity abstract (optional)

    cand_dis_by_context_score = 0  # score from disambiguation by context
    cand_dis_by_levenshtein_score = 0  # score from disambiguation by levenshtein distance
