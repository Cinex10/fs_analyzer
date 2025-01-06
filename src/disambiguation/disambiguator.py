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
    
    def disambiguate_all(self, words):
        res = {}
        for i in range(len(words) - 1):
            word = words[i]
            next_word = words[i+1]
            relation = self.disambiguate(word, next_word)
            if relation:
                res[word] = [relation]
        return res
    
    