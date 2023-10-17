from named_entity_recognition.NER_using_spacy import *
from candidate_generation.candidate_generation import *

if __name__ == "__main__":
    text = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."
    text_mj = 'Michael Jeffrey Jordan (born February 17, 1963), also known by his initials MJ, is an American former professional basketball player and businessman. His profile on the official National Basketball Association (NBA) website states that "by acclamation, Michael Jordan is the greatest basketball player of all time." He played fifteen seasons in the NBA, winning six NBA championships with the Chicago Bulls. He was integral in popularizing the sport of basketball and the NBA around the world in the 1980s and 1990s, becoming a global cultural icon.'
    text_sgfm = "Camp Nou, officially branded as Spotify Camp Nou for sponsorship and financial reasons, is a football stadium in Barcelona, Spain."

    entities = named_entity_recognition_using_spacy(text_sgfm)

    for entity in entities:
        entity = map_entity_type_to_dbpedia_ontology(entity)
        query_result = query_dbpedia(entity)
        # print(query_result)

        entity = save_found_candidates(query_result, entity)
        # entity = sort_cand_by_ont_depth(entity)
        # entity = extract_deepest_candidates(entity)

    # Print the remaining candidates for each entity
    for entity in entities:
        print(f"\nEntity \"{entity.surface_form}\"")
        print(f"ont_type_spacy \"{entity.ont_type_spacy}\"")
        print(f"ont_type_dbpedia \"{entity.ont_type_dbpedia}\"")
        print(f"Candidates ({len(entity.candidates)}):")
        for candidate in entity.candidates:
            print(f"\tName: {candidate.label}, URI: {candidate.uri}")
        print("\n")
