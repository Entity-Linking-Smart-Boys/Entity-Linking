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
    entities = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
    # print(entities)  # [('Nikola Tesla', 0, 12, 'PERSON'), ('Serbian', 14, 21, 'NORP'), ('Тесла', 39, 44, 'PERSON'), ('Serbian', 52, 59, 'NORP')]
    # displacy allows to see the text in a user-friendly form with tagged entities
    # print(doc.ents)  # (Nikola Tesla, Serbian, Тесла, Serbian)
    displacy.render(doc, style='ent')

    return list(doc.ents)
