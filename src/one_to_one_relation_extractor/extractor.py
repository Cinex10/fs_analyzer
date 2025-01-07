import pdb
from data.jdm_client import JdmApiClient
from data.relation_types_mapper import RelationTypesMapper
from data.node_types_mapper import NodeTypesMapper


class OneToOneRelationExtractor:
    def __init__(self, allowed_relations = [4, 19]):
        self.client = JdmApiClient()
        self.relation_types = RelationTypesMapper()
        self.node_types = NodeTypesMapper()
        self.allowed_relations = allowed_relations

    def tag(self, words):
        sentence = ' '.join(words)
        word_relation_map = {}
        tagging_res = {}
        compound_words_detection_res = []
        for word in words:
            relations = self.client.get_from_relations(word)
            word_relation_map[word] = relations
        
            for relation_data in relations:
                if relation_data['relation']['type'] in self.allowed_relations and relation_data['relation']['w'] > 0 and relation_data['node']['name'].endswith(':') and len(relation_data['node']['name'].split(':')) == 2:
                        tagging_res[word] = tagging_res.get(word, []) + [{
                            'relation_type' : self.relation_types.get_word(relation_data['relation']['type']),
                            'to_node_name' : relation_data['node']['name'],
                            'to_node_type' : self.node_types.get_word(relation_data['node']['type']),
                        }]
                # pdb.set_trace()
                try:
                    compound_word = relation_data['node']['name']
                    fragments = compound_word.split()
                except:
                     print(fragments)
                if len(fragments) > 1 and compound_word in sentence:
                    compound_words_detection_res.append({
                        "compound_word": fragments
                    })
        return tagging_res , compound_words_detection_res
    