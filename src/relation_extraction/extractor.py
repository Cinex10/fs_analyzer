from src.data.jdm_client import JdmApiClient


class RelationExtractor:
    def __init__(self):
        self.client = JdmApiClient()
        
    def extract_from_relation(self, words):
        res = {}
        for word in words:
            res[word] = self.client.get_from_relations(word)
        return res