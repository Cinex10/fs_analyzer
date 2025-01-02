from src.data.jdm_client import JdmApiClient


class PosTagger:
    def __init__(self):
        self.client = JdmApiClient()

    def tag(self, word_relation_map):
        res = {}
        for word, relations in word_relation_map.items():
            tmp = []
            for relation in relations:
                if relation.type == 4:
                    tmp.append((relation, self.client.get_pos_tag(word, relation)))
            res[word] = tmp
        return res
    