from data.jdm_client import JdmApiClient
from data.relation_types_mapper import RelationTypesMapper
from data.node_types_mapper import NodeTypesMapper


class OneToOneRelationExtractor:
    def __init__(self):
        self.client = JdmApiClient()
        self.relation_types = RelationTypesMapper()
        self.node_types = NodeTypesMapper()
        self.allowed_relations = [4, 19]

    def tag(self, words):
        word_relation_map = {}
        res = {}
        for word in words:
            relations = self.client.get_from_relations(word)
            word_relation_map[word] = relations
        
            for relation_data in relations:
                if relation_data['relation']['type'] in self.allowed_relations:
                        relation_data = {
                            'relation_type' : self.relation_types.get_word(relation_data['relation']['type']),
                            'to_node_name' : relation_data['node']['name'],
                            'to_node_type' : self.node_types.get_word(relation_data['node']['type']),
                        }
                        res[word] = res.get(word, []) + [relation_data]
        return res
    