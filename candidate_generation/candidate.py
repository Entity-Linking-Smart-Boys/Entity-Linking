class Candidate:
    def __init__(self, uri, label, ont_type):
        self.uri = uri  # from DBpedia - link to the page with details
        self.label = label
        self.ont_type = ont_type
