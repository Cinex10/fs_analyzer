import pdb
from data.disambiguator_data import DisambiguatorData


class Disambiguator:
    def __init__(self):
        self.data = DisambiguatorData()
    
    def disambiguate(self, word, next_word):
        if not next_word:
            return None
        raff = self.data.get_raff(word)
        for r in raff:
            if r['ref'].split('>')[-1] == next_word:
                return {
                        'relation_type' : 'r_raff_sem',
                        'to_node_name' : r['ref'].split('>')[1],
                        'to_node_type' : 'n_term',
                    }