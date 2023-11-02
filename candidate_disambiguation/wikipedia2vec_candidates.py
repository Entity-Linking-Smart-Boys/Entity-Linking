# https://wikipedia2vec.github.io/wikipedia2vec/commands/
# https://aclanthology.org/2020.emnlp-demos.4.pdf

# TODO: install the file:
# $ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
# $ wikipedia2vec train enwiki-latest-pages-articles.xml.bz2 MODEL_FILE

# Wikipedia2Vec
from wikipedia2vec import Wikipedia2Vec


# return the top N candidate entities based on their similarity to the mention
def link_entities_with_wikipedia2vec(wiki2vec, mention, candidate_entities, top_n=1):
    """
    Links a mention to candidate entities using Wikipedia2Vec.

    Args:
        mention (str): The mention to be linked to entities.
        candidate_entities (list): List of candidate entity titles.
        top_n (int, optional): The number of top candidate entities to return. Default is 1.

    Returns:
        list: A list of the top N candidate entities based on similarity to the mention.
    """
    entity_similarities = []

    for entity in candidate_entities:
        # Calculate similarity between the mention and candidate entity
        similarity = wiki2vec.get_entity_similarity(mention, entity)

        entity_similarities.append((entity, similarity))

    # Sort candidate entities by similarity in descending order
    entity_similarities.sort(key=lambda x: x[1], reverse=True)

    # Select the top N entities with the highest similarity
    top_entities = [entity for entity, _ in entity_similarities[:top_n]]

    return top_entities


if __name__ == "__main__":
    wiki2vec = Wikipedia2Vec.load(MODEL_FILE)
    wiki2vec.get_entity_vector("Scarlett Johansson")
    wiki2vec.most_similar(model.get_entity("Python (programming language)"))[:3]
