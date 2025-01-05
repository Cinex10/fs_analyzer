from data.jdm_client import JdmApiClient
from data.relation_types_mapper import RelationTypesMapper
from data.node_types_mapper import NodeTypesMapper


class PosTagger:
    def __init__(self):
        self.client = JdmApiClient()
        self.relation_types = RelationTypesMapper()
        self.node_types = NodeTypesMapper()

    def tag(self, word_relation_map):
        res = {}
        for wo, data in word_relation_map.items():
            for tmp in data:
                if tmp['relation']['type'] == 4:
                    # try:
                        relation_data = {
                            'relation_type' : self.relation_types.get_word(tmp['relation']['type']),
                            'to_node_name' : tmp['node']['name'],
                            'to_node_type' : self.node_types.get_word(tmp['node']['type']),
                        }
                        res[wo] = res.get(wo, []) + [relation_data]
        return res
    