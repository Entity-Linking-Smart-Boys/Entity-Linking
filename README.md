# Entity-Linking

Entity linking consists of several steps:
- [Named Entity Recognition (NER)](#named-entity-recognition-ner)
- [Candidate generation](#candidate-generation)
- [Candidate disambiguation](#candidate-disambiguation)


## Named Entity Recognition (NER)
It is the process of identifying the key information in the text.
Each piece of information is classified into a set of predefined categories such as people, organizations, and locations.
An entity is the thing that is consistently talked about or referred to in the particular text.

### Three main steps
NER consists of three main steps: 
1. **Tokenization**, which involves breaking the text into individual words or phrases.
2. **Part-of-speech tagging**, which assigns a grammatical tag to each word.
3. **Entity recognition**, which identifies and classifies the named entities in the text.

Suppose we have the following sentence: "Apple Inc. was founded by Steve Jobs in Cupertino, California."
The process of NER would look like this:
1. **Tokenization**:
    "Apple"
    "Inc."
    "was"
    "founded"
    "by"
    "Steve"
    "Jobs"
    "in"
    "Cupertino"
    "California"
2. **Part-of-speech tagging**:
    "Apple" - Noun (specifically, a proper noun)
    "Inc." - Noun
    "was" - Verb
    "founded" - Verb
    "by" - Preposition
    "Steve" - Noun (a person's name)
    "Jobs" - Noun (a person's name)
    "in" - Preposition
    "Cupertino" - Noun (a location name)
    "California" - Noun (a location name)
3. **Entity recognition**:
    "Apple Inc." - This is an organization name.
    "Steve Jobs" - This is a person's name.
    "Cupertino" - This is a location name.
    "California" - This is another location name.


### Model
In this project Deep Learning Based NER is used.
It uses machine learning algorithms to analyze text and identify patterns that indicate the presence of named entities.
These algorithms are trained on large datasets of annotated text, where human annotators have labeled the named entities in the text.
SpaCy NER uses a method called word embedding, that is capable of understanding the semantic and syntactic relationship between various words

SpaCy allows using their [Trained Models & Pipelines](https://spacy.io/models).
Currently, in this project the model [en_core_web_lg](https://spacy.io/models/en#en_core_web_lg) is used.
It can be downloaded using the following command:
```bash
python -m spacy download en_core_web_lg
```
After that the package is loaded in the Python file via
```python 
spacy.load('en_core_web_sm')
```

### Entity tags
Below is a list and the meaning of SpaCy entity tags, which are used during the process of classification of the entities:

![NER_spacy_entity_tags.png](readme_images/NER_spacy_entity_tags.png)

### Output
For each entity the systems returns:
- the surface form (text) of the entity
- the number of the starting character
- the number of the ending character
- the label, which is the name of one of the predefined classes

For example for the text:
```text
Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system.
```

The entities would be:
```text
[('Nikola Tesla', 0, 12, 'PERSON'),
('Serbian', 14, 21, 'NORP'),
('Тесла', 39, 44, 'PERSON'),
('Serbian', 52, 59, 'NORP')]
(Nikola Tesla, Serbian, Тесла, Serbian)
```

The labelled text looks like this:

![NER_labelled_text.png](readme_images/NER_labelled_text.png)


## Candidate generation

### DBpedia ontology

The documentation of DBpedia ontology is available online [here](https://www.dbpedia.org/resources/ontology/).
Visualised ontology is available online [here](https://service.tib.eu/webvowl/#iri=https://akswnc7.informatik.uni-leipzig.de/dstreitmatter/archivo/dbpedia.org/ontology--DEV/2023.04.20-002000/ontology--DEV_type=parsed.owl).

[//]: # (The ontology can be loaded from a file using [owlready2]&#40;https://owlready2.readthedocs.io/en/latest/onto.html&#41;.)

[SPARQL](https://www.ontotext.com/knowledgehub/fundamentals/what-is-sparql/) can be used to query the ontology.
[SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/main.html) allows connecting to a specific URL and query the data. 


